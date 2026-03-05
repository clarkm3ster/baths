"""Tests for the DOMES cross-reference engine."""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.circumstances import CrossReference
from app.cross_reference import (
    build_cross_references,
    _extract_usc_parts,
    _extract_cfr_parts,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _prov(id, citation, title, domain, ptype, applies_when, enforcement=None, xrefs=None, full_text=""):
    return {
        "id": id,
        "citation": citation,
        "title": title,
        "full_text": full_text,
        "domain": domain,
        "provision_type": ptype,
        "applies_when": json.dumps(applies_when),
        "enforcement_mechanisms": json.dumps(enforcement or []),
        "cross_references": json.dumps(xrefs or []),
    }


# ---------------------------------------------------------------------------
# Citation parsing tests
# ---------------------------------------------------------------------------

class TestCitationParsing:
    def test_usc_standard_format(self):
        parts = _extract_usc_parts("42 U.S.C. § 1396d(r)")
        assert ("42", "1396d") in parts

    def test_usc_multiple(self):
        parts = _extract_usc_parts("42 U.S.C. § 12132 and 29 U.S.C. § 794")
        assert ("42", "12132") in parts
        assert ("29", "794") in parts

    def test_cfr_part_format(self):
        parts = _extract_cfr_parts("42 CFR Part 438")
        assert ("42", "438") in parts

    def test_cfr_part_keyword_format(self):
        parts = _extract_cfr_parts("28 CFR Part 35")
        assert ("28", "35") in parts

    def test_cfr_section_symbol_format(self):
        parts = _extract_cfr_parts("28 CFR § 35.130")
        assert ("28", "35") in parts

    def test_no_match_returns_empty(self):
        assert _extract_usc_parts("Olmstead v. L.C.") == []
        assert _extract_cfr_parts("U.S. Constitution") == []


# ---------------------------------------------------------------------------
# Statute-to-regulation linking tests
# ---------------------------------------------------------------------------

class TestStatuteRegulationLinks:
    def test_medicaid_statute_links_to_cfr(self):
        provs = [
            _prov(1, "42 U.S.C. § 1396a(a)(10)", "Medicaid Statute", "health", "right",
                  {"insurance": ["medicaid"]}),
            _prov(2, "42 CFR Part 438", "Medicaid Managed Care Regs", "health", "obligation",
                  {"insurance": ["medicaid"]}),
        ]
        xrefs = build_cross_references(provs)
        assert 1 in xrefs
        links_from_statute = [x for x in xrefs[1] if x.relationship == "implements"]
        assert len(links_from_statute) >= 1
        assert any(x.target_id == 2 for x in links_from_statute)

    def test_ada_statute_links_to_regulation(self):
        provs = [
            _prov(10, "42 U.S.C. § 12132", "ADA Title II", "civil_rights", "right",
                  {"disabilities": ["any"]}),
            _prov(11, "28 CFR Part 35", "ADA Title II Regulations", "civil_rights", "obligation",
                  {"disabilities": ["any"]}),
        ]
        xrefs = build_cross_references(provs)
        assert 10 in xrefs
        links = [x for x in xrefs[10] if x.target_id == 11]
        assert len(links) >= 1
        assert links[0].relationship == "implements"

    def test_bidirectional_links(self):
        """Both statute and regulation should link to each other."""
        provs = [
            _prov(1, "42 U.S.C. § 1396d(r)", "EPSDT", "health", "right",
                  {"insurance": ["medicaid"]}),
            _prov(2, "42 CFR Part 441", "EPSDT Regs", "health", "obligation",
                  {"insurance": ["medicaid"]}),
        ]
        xrefs = build_cross_references(provs)
        assert 1 in xrefs
        assert 2 in xrefs
        assert any(x.target_id == 2 for x in xrefs[1])
        assert any(x.target_id == 1 for x in xrefs[2])

    def test_idea_links_to_regulation(self):
        provs = [
            _prov(20, "20 U.S.C. § 1400", "IDEA", "education", "right",
                  {"disabilities": ["any"], "age": ["3_to_21"]}),
            _prov(21, "34 CFR Part 300", "IDEA Regulations", "education", "obligation",
                  {"disabilities": ["any"], "age": ["3_to_21"]}),
        ]
        xrefs = build_cross_references(provs)
        assert 20 in xrefs
        assert any(x.target_id == 21 for x in xrefs[20])

    def test_snap_statute_to_regulation(self):
        provs = [
            _prov(30, "7 U.S.C. § 2011", "SNAP", "income", "right",
                  {"income": ["below_poverty"]}),
            _prov(31, "7 CFR Part 273", "SNAP Regs", "income", "obligation",
                  {"income": ["below_poverty"]}),
        ]
        xrefs = build_cross_references(provs)
        assert 30 in xrefs
        assert any(x.target_id == 31 for x in xrefs[30])


# ---------------------------------------------------------------------------
# Explicit cross_references field tests
# ---------------------------------------------------------------------------

class TestExplicitCrossReferences:
    def test_cross_reference_field_respected(self):
        provs = [
            _prov(1, "42 U.S.C. § 1396d(r)", "EPSDT", "health", "right",
                  {"insurance": ["medicaid"]},
                  xrefs=["42 U.S.C. § 1396a(a)(43)"]),
            _prov(2, "42 U.S.C. § 1396a(a)(43)", "EPSDT Outreach", "health", "obligation",
                  {"insurance": ["medicaid"]}),
        ]
        xrefs = build_cross_references(provs)
        assert 1 in xrefs
        related = [x for x in xrefs[1] if x.target_id == 2]
        assert len(related) >= 1

    def test_cross_reference_nonexistent_citation_ignored(self):
        provs = [
            _prov(1, "42 U.S.C. § 1396d(r)", "EPSDT", "health", "right",
                  {"insurance": ["medicaid"]},
                  xrefs=["99 U.S.C. § 99999"]),
        ]
        xrefs = build_cross_references(provs)
        # Should not crash, and should have no refs since target doesn't exist
        refs = xrefs.get(1, [])
        assert not any(x.target_citation == "99 U.S.C. § 99999" for x in refs)

    def test_self_reference_excluded(self):
        provs = [
            _prov(1, "42 U.S.C. § 1396d(r)", "EPSDT", "health", "right",
                  {"insurance": ["medicaid"]},
                  xrefs=["42 U.S.C. § 1396d(r)"]),
        ]
        xrefs = build_cross_references(provs)
        refs = xrefs.get(1, [])
        assert not any(x.target_id == 1 for x in refs)


# ---------------------------------------------------------------------------
# Same-domain overlap tests
# ---------------------------------------------------------------------------

class TestSameDomainOverlap:
    def test_overlapping_conditions_linked(self):
        """Two health provisions sharing insurance+age conditions should be related."""
        provs = [
            _prov(1, "Provision A", "Health Right A", "health", "right",
                  {"insurance": ["medicaid"], "age": ["under_21"]}),
            _prov(2, "Provision B", "Health Right B", "health", "right",
                  {"insurance": ["medicaid"], "age": ["under_21"], "disabilities": ["any"]}),
        ]
        xrefs = build_cross_references(provs)
        assert 1 in xrefs
        assert any(x.target_id == 2 and x.relationship == "related" for x in xrefs[1])

    def test_different_domains_not_linked_by_overlap(self):
        """Provisions in different domains should not be linked by condition overlap."""
        provs = [
            _prov(1, "Health A", "Health Right", "health", "right",
                  {"insurance": ["medicaid"], "age": ["under_21"]}),
            _prov(2, "Education A", "Education Right", "education", "right",
                  {"insurance": ["medicaid"], "age": ["under_21"]}),
        ]
        xrefs = build_cross_references(provs)
        # Should not link across domains via overlap logic
        if 1 in xrefs:
            assert not any(
                x.target_id == 2 and x.relationship == "related"
                for x in xrefs[1]
            )

    def test_single_key_overlap_not_linked(self):
        """Only one overlapping key is not enough for 'related' (need >= 2)."""
        provs = [
            _prov(1, "A", "Right A", "health", "right",
                  {"insurance": ["medicaid"]}),
            _prov(2, "B", "Right B", "health", "right",
                  {"insurance": ["medicaid"]}),
        ]
        xrefs = build_cross_references(provs)
        if 1 in xrefs:
            assert not any(
                x.target_id == 2 and x.relationship == "related"
                for x in xrefs[1]
            )

    def test_no_value_overlap_not_linked(self):
        """Same keys but different values should not link."""
        provs = [
            _prov(1, "A", "Right A", "health", "right",
                  {"insurance": ["medicaid"], "age": ["under_21"]}),
            _prov(2, "B", "Right B", "health", "right",
                  {"insurance": ["medicare"], "age": ["65_plus"]}),
        ]
        xrefs = build_cross_references(provs)
        if 1 in xrefs:
            assert not any(x.target_id == 2 for x in xrefs[1])


# ---------------------------------------------------------------------------
# Deduplication tests
# ---------------------------------------------------------------------------

class TestDeduplication:
    def test_no_duplicate_references(self):
        """Same provision pair should not have duplicate references of same type."""
        provs = [
            _prov(1, "42 U.S.C. § 1396a(a)(10)", "Medicaid", "health", "right",
                  {"insurance": ["medicaid"], "age": ["under_21"]},
                  xrefs=["42 CFR Part 438"]),
            _prov(2, "42 CFR Part 438", "Managed Care", "health", "obligation",
                  {"insurance": ["medicaid"], "age": ["under_21"]}),
        ]
        xrefs = build_cross_references(provs)
        if 1 in xrefs:
            pairs = [(x.target_id, x.relationship) for x in xrefs[1]]
            assert len(pairs) == len(set(pairs))


# ---------------------------------------------------------------------------
# Real seed data integration test
# ---------------------------------------------------------------------------

class TestWithSeedData:
    def _get_seed_provisions(self):
        from app.seed import PROVISIONS
        provs = []
        for i, p in enumerate(PROVISIONS, 1):
            d = dict(p)
            d["id"] = i
            provs.append(d)
        return provs

    def test_seed_data_produces_cross_references(self):
        provs = self._get_seed_provisions()
        xrefs = build_cross_references(provs)
        assert len(xrefs) > 0, "Should find some cross-references in seed data"

    def test_medicaid_provisions_are_cross_referenced(self):
        provs = self._get_seed_provisions()
        xrefs = build_cross_references(provs)
        # Find the EPSDT provision (42 U.S.C. § 1396d(r))
        epsdt_id = None
        for p in provs:
            if "1396d(r)" in p["citation"]:
                epsdt_id = p["id"]
                break
        if epsdt_id and epsdt_id in xrefs:
            assert len(xrefs[epsdt_id]) >= 1, (
                "EPSDT should have at least one cross-reference"
            )
