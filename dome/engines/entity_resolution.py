"""Entity resolution engine for THE DOME (Step 1).

Implements probabilistic record linkage using Fellegi-Sunter methodology
to consolidate fragmented person records from multiple public-system silos
into a single IdentitySpine.  Each record pair is scored on agreement/
disagreement across name hash, date of birth, SSN hash, and address
similarity; pairs exceeding the match threshold are merged into a single
resolved identity.

Usage::

    resolver = EntityResolver()
    result = resolver.resolve(records)
    # result contains 'spine', 'cross_system_ids', 'linkage_confidence_by_system'
"""

from __future__ import annotations

import math
from collections import defaultdict
from datetime import date
from typing import Any


# ---------------------------------------------------------------------------
# Fellegi-Sunter weight configuration
# ---------------------------------------------------------------------------

# Each field has:
#   m = P(field agrees | records are a true match)
#   u = P(field agrees | records are NOT a match)
# Match weight   = log2(m / u)
# Non-match weight = log2((1-m) / (1-u))

_FIELD_PARAMS: dict[str, dict[str, float]] = {
    "name_hash": {"m": 0.92, "u": 0.01},
    "dob": {"m": 0.95, "u": 0.002},
    "ssn_hash": {"m": 0.98, "u": 0.0001},
    "address_hash": {"m": 0.80, "u": 0.05},
}

# Pre-compute match and non-match weights
_MATCH_WEIGHTS: dict[str, float] = {}
_NON_MATCH_WEIGHTS: dict[str, float] = {}

for _field, _params in _FIELD_PARAMS.items():
    _m, _u = _params["m"], _params["u"]
    _MATCH_WEIGHTS[_field] = math.log2(_m / _u)
    _NON_MATCH_WEIGHTS[_field] = math.log2((1 - _m) / (1 - _u))


def _compute_match_weight() -> float:
    """Maximum possible composite weight when all fields agree."""
    return sum(_MATCH_WEIGHTS.values())


def _compute_non_match_weight() -> float:
    """Minimum possible composite weight when all fields disagree."""
    return sum(_NON_MATCH_WEIGHTS.values())


# Thresholds expressed as fractions of the max possible match weight
_MAX_WEIGHT = _compute_match_weight()
_MATCH_THRESHOLD = 0.65 * _MAX_WEIGHT     # Above this -> definite match
_CLERICAL_THRESHOLD = 0.40 * _MAX_WEIGHT   # Between clerical & match -> possible


class EntityResolver:
    """Probabilistic entity resolution engine using Fellegi-Sunter matching.

    Ingests a list of person-record dicts from disparate systems and
    produces a consolidated identity result containing:
    - A canonical IdentitySpine dict
    - Merged cross-system IDs
    - Per-system linkage confidence scores

    Each input record should contain some subset of::

        {
            "system": str,           # originating system name
            "record_id": str,        # ID within that system
            "name_hash": str,        # one-way hash of canonical name
            "dob": str | date,       # date of birth (ISO or date object)
            "ssn_hash": str | None,  # one-way hash of SSN
            "address_hash": str | None,  # hash of street-level address
            "address_city": str | None,
            "address_state": str | None,
            "address_zip5": str | None,
            "address_tract_fips": str | None,
            "sex_at_birth": str,
            ...additional system-specific ID fields...
        }
    """

    def __init__(
        self,
        match_threshold: float | None = None,
        clerical_threshold: float | None = None,
    ) -> None:
        """Initialise the resolver with optional custom thresholds.

        Parameters
        ----------
        match_threshold:
            Composite Fellegi-Sunter weight above which two records are
            considered a definite match.  Defaults to 65% of max weight.
        clerical_threshold:
            Weight above which a pair is flagged for clerical review.
            Defaults to 40% of max weight.
        """
        self.match_threshold = match_threshold or _MATCH_THRESHOLD
        self.clerical_threshold = clerical_threshold or _CLERICAL_THRESHOLD

    # ------------------------------------------------------------------ #
    #  Public API
    # ------------------------------------------------------------------ #

    def resolve(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        """Resolve a set of records into a single identity result.

        Parameters
        ----------
        records:
            List of dicts, each representing a person record from a
            single source system.

        Returns
        -------
        dict with keys:
            spine: dict
                Canonical IdentitySpine-compatible dict.
            cross_system_ids: dict
                Merged cross-system identifiers from all matched records.
            linkage_confidence_by_system: dict[str, float]
                Per-system linkage confidence (0.0 - 1.0).
            clusters: list[list[int]]
                Indices into the original record list grouped by resolved
                identity.  When all records belong to one person, there
                is a single cluster.
            match_pairs: list[dict]
                Detail of every pairwise comparison that exceeded the
                clerical threshold.
        """
        if not records:
            return {
                "spine": {},
                "cross_system_ids": {},
                "linkage_confidence_by_system": {},
                "clusters": [],
                "match_pairs": [],
            }

        # Normalise records
        normalised = [self._normalise_record(r) for r in records]

        # Pairwise comparison
        pair_scores = self._pairwise_compare(normalised)

        # Cluster via union-find
        clusters = self._cluster(len(normalised), pair_scores)

        # Build identity spine from the largest cluster
        primary_cluster = max(clusters, key=len)
        primary_records = [normalised[i] for i in primary_cluster]

        spine = self._build_spine(primary_records)
        cross_ids = self._merge_cross_system_ids(primary_records)
        confidences = self._compute_system_confidences(
            primary_records, pair_scores, primary_cluster,
        )

        spine["cross_system_ids"] = cross_ids
        spine["linkage_confidence_by_system"] = confidences

        return {
            "spine": spine,
            "cross_system_ids": cross_ids,
            "linkage_confidence_by_system": confidences,
            "clusters": [sorted(c) for c in clusters],
            "match_pairs": [
                p for p in pair_scores if p["weight"] >= self.clerical_threshold
            ],
        }

    # ------------------------------------------------------------------ #
    #  Record normalisation
    # ------------------------------------------------------------------ #

    @staticmethod
    def _normalise_record(record: dict[str, Any]) -> dict[str, Any]:
        """Normalise a raw input record to a standard internal format."""
        out = dict(record)

        # Ensure dob is a date object
        if isinstance(out.get("dob"), str):
            out["dob"] = date.fromisoformat(out["dob"])

        # Normalise missing values to None
        for key in ("name_hash", "ssn_hash", "address_hash"):
            if key in out and out[key] in ("", "null", "NA"):
                out[key] = None

        return out

    # ------------------------------------------------------------------ #
    #  Pairwise comparison (Fellegi-Sunter)
    # ------------------------------------------------------------------ #

    def _pairwise_compare(
        self, records: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Compare every pair of records and compute composite weights.

        Returns a list of score dicts for pairs that exceed the clerical
        threshold.
        """
        results: list[dict[str, Any]] = []
        n = len(records)
        for i in range(n):
            for j in range(i + 1, n):
                weight, field_scores = self._compare_pair(records[i], records[j])
                if weight >= self.clerical_threshold:
                    results.append({
                        "i": i,
                        "j": j,
                        "weight": weight,
                        "is_match": weight >= self.match_threshold,
                        "field_scores": field_scores,
                    })
        return results

    def _compare_pair(
        self,
        a: dict[str, Any],
        b: dict[str, Any],
    ) -> tuple[float, dict[str, float]]:
        """Compute the Fellegi-Sunter composite weight for a record pair.

        Returns
        -------
        (composite_weight, per_field_weights)
        """
        total = 0.0
        field_scores: dict[str, float] = {}

        for field in _FIELD_PARAMS:
            val_a = a.get(field)
            val_b = b.get(field)

            if val_a is None or val_b is None:
                # Missing data: contribute zero weight (no information)
                field_scores[field] = 0.0
                continue

            if field == "dob":
                agrees = self._dob_agrees(val_a, val_b)
            elif field == "address_hash":
                agrees = self._address_agrees(a, b)
            else:
                # Exact string match for hashed fields
                agrees = val_a == val_b

            if agrees:
                w = _MATCH_WEIGHTS[field]
            else:
                w = _NON_MATCH_WEIGHTS[field]

            field_scores[field] = w
            total += w

        return total, field_scores

    @staticmethod
    def _dob_agrees(dob_a: date, dob_b: date) -> bool:
        """Two DOBs agree if they are identical.

        A future refinement could grant partial credit for transposition
        errors (e.g. month/day swap), but for now we require exact match.
        """
        return dob_a == dob_b

    @staticmethod
    def _address_agrees(a: dict[str, Any], b: dict[str, Any]) -> bool:
        """Address agreement with multi-level fallback.

        Checks address_hash first, then falls back to zip5, then state.
        This gives partial credit when a person has moved but stays in
        the same geography.
        """
        hash_a = a.get("address_hash")
        hash_b = b.get("address_hash")

        if hash_a is not None and hash_b is not None and hash_a == hash_b:
            return True

        # Fall back: same ZIP code counts as agreement for address field
        zip_a = a.get("address_zip5")
        zip_b = b.get("address_zip5")
        if zip_a and zip_b and zip_a == zip_b:
            return True

        return False

    # ------------------------------------------------------------------ #
    #  Union-Find clustering
    # ------------------------------------------------------------------ #

    @staticmethod
    def _cluster(
        n: int, pair_scores: list[dict[str, Any]]
    ) -> list[list[int]]:
        """Cluster record indices using union-find on matched pairs.

        Parameters
        ----------
        n:
            Total number of records.
        pair_scores:
            Pairwise scores from ``_pairwise_compare``; only pairs with
            ``is_match=True`` are linked.

        Returns
        -------
        List of clusters, where each cluster is a list of record indices.
        """
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path compression
                x = parent[x]
            return x

        def union(x: int, y: int) -> None:
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            if rank[rx] < rank[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            if rank[rx] == rank[ry]:
                rank[rx] += 1

        for pair in pair_scores:
            if pair["is_match"]:
                union(pair["i"], pair["j"])

        # Group by root
        groups: dict[int, list[int]] = defaultdict(list)
        for i in range(n):
            groups[find(i)].append(i)

        return list(groups.values())

    # ------------------------------------------------------------------ #
    #  Spine construction
    # ------------------------------------------------------------------ #

    @staticmethod
    def _build_spine(records: list[dict[str, Any]]) -> dict[str, Any]:
        """Build a canonical IdentitySpine dict from a cluster of records.

        Uses majority-vote / most-frequent-value logic for each field.
        For date of birth and name hash the most common value wins.
        Address history is aggregated from all records.
        """
        # Pick canonical values by frequency
        name_counts: dict[str, int] = defaultdict(int)
        dob_counts: dict[date, int] = defaultdict(int)
        sex_counts: dict[str, int] = defaultdict(int)
        ssn_hashes: dict[str, int] = defaultdict(int)
        addresses: list[dict[str, Any]] = []

        for rec in records:
            nh = rec.get("name_hash")
            if nh:
                name_counts[nh] += 1

            dob_val = rec.get("dob")
            if isinstance(dob_val, date):
                dob_counts[dob_val] += 1

            sex = rec.get("sex_at_birth")
            if sex:
                sex_counts[sex] += 1

            ssh = rec.get("ssn_hash")
            if ssh:
                ssn_hashes[ssh] += 1

            # Collect address info if present
            if rec.get("address_hash"):
                addr = {
                    "street_hash": rec.get("address_hash", ""),
                    "city": rec.get("address_city", ""),
                    "state": rec.get("address_state", ""),
                    "zip5": rec.get("address_zip5", ""),
                    "tract_fips": rec.get("address_tract_fips", ""),
                }
                if addr not in addresses:
                    addresses.append(addr)

        def _most_common(counts: dict) -> Any:
            if not counts:
                return None
            return max(counts, key=counts.get)  # type: ignore[arg-type]

        canonical_name = _most_common(name_counts) or ""
        canonical_dob = _most_common(dob_counts) or date(1900, 1, 1)
        canonical_sex = _most_common(sex_counts) or "unknown"
        canonical_ssn = _most_common(ssn_hashes)

        return {
            "name_hash": canonical_name,
            "dob": canonical_dob.isoformat() if isinstance(canonical_dob, date) else str(canonical_dob),
            "sex_at_birth": canonical_sex,
            "ssn_hash": canonical_ssn,
            "address_history": addresses,
        }

    # ------------------------------------------------------------------ #
    #  Cross-system ID merging
    # ------------------------------------------------------------------ #

    # Known cross-system ID field names (matching CrossSystemIds model)
    _CROSS_SYSTEM_FIELDS = (
        "ssn_hash",
        "irs_tin_hash",
        "ssa_beneficiary_id",
        "medicare_id",
        "medicaid_id",
        "chip_id",
        "snap_case_id",
        "tanf_case_id",
        "hud_client_id",
        "pha_household_id",
        "hmis_id",
        "state_prison_id",
        "county_jail_id",
        "court_case_ids",
        "school_district_student_id",
        "higher_ed_student_id",
        "unemployment_insurance_id",
        "wioa_participant_id",
        "va_id",
    )

    @classmethod
    def _merge_cross_system_ids(
        cls, records: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Merge cross-system identifiers from all matched records.

        For scalar ID fields, the first non-None value is used.
        For list fields (e.g. court_case_ids), values are concatenated
        and deduplicated.
        """
        merged: dict[str, Any] = {}
        for field in cls._CROSS_SYSTEM_FIELDS:
            if field == "court_case_ids":
                # Aggregate list field
                all_ids: list[str] = []
                for rec in records:
                    val = rec.get(field)
                    if isinstance(val, list):
                        all_ids.extend(val)
                    elif isinstance(val, str) and val:
                        all_ids.append(val)
                merged[field] = list(dict.fromkeys(all_ids))  # dedup preserving order
            else:
                # Scalar field: take first non-None
                merged[field] = None
                for rec in records:
                    val = rec.get(field)
                    if val is not None and val != "":
                        merged[field] = val
                        break

        # Also merge system-specific record_id references
        system_ids: dict[str, str] = {}
        for rec in records:
            sys = rec.get("system")
            rid = rec.get("record_id")
            if sys and rid:
                system_ids[sys] = rid
        merged["_source_system_ids"] = system_ids

        return merged

    # ------------------------------------------------------------------ #
    #  Confidence computation
    # ------------------------------------------------------------------ #

    def _compute_system_confidences(
        self,
        records: list[dict[str, Any]],
        pair_scores: list[dict[str, Any]],
        cluster_indices: list[int],
    ) -> dict[str, float]:
        """Compute per-system linkage confidence scores.

        For each system represented in the cluster, confidence is derived
        from the best pairwise Fellegi-Sunter weight involving a record
        from that system, normalised to [0, 1].

        If only one system is present, confidence is 1.0 (self-link).
        """
        # Map record index -> system name
        idx_to_system: dict[int, str] = {}
        for idx, rec in zip(cluster_indices, records):
            sys = rec.get("system", f"unknown_{idx}")
            idx_to_system[idx] = sys

        systems_in_cluster = set(idx_to_system.values())
        cluster_set = set(cluster_indices)

        # Best weight per system pair
        best_weight_by_system: dict[str, float] = {s: 0.0 for s in systems_in_cluster}

        for pair in pair_scores:
            if not pair["is_match"]:
                continue
            i, j = pair["i"], pair["j"]
            if i not in cluster_set or j not in cluster_set:
                continue

            sys_i = idx_to_system.get(i)
            sys_j = idx_to_system.get(j)
            weight = pair["weight"]

            if sys_i and weight > best_weight_by_system.get(sys_i, 0.0):
                best_weight_by_system[sys_i] = weight
            if sys_j and weight > best_weight_by_system.get(sys_j, 0.0):
                best_weight_by_system[sys_j] = weight

        # Normalise weights to [0, 1] using sigmoid-like mapping
        confidences: dict[str, float] = {}
        for system, best_w in best_weight_by_system.items():
            if best_w <= 0:
                # No cross-system link found; if single-system, full confidence
                if len(systems_in_cluster) == 1:
                    confidences[system] = 1.0
                else:
                    confidences[system] = 0.0
            else:
                # Normalise: weight / max_possible_weight, clamped to [0, 1]
                raw = best_w / _MAX_WEIGHT if _MAX_WEIGHT > 0 else 0.0
                confidences[system] = min(max(raw, 0.0), 1.0)

        return confidences
