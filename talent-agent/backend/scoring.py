"""
Chron Talent Agent — Dimension-Based Scoring

Cosm (DOMES) — 6 dimensions:
  Rights, Research, Budget, Package, Deliverables, Pitch
  Total Cosm = minimum across all 6 dimensions.
  The dome is only as strong as its weakest face.

Chron (SPHERES) — 5 dimensions:
  Unlock, Access, Permanence, Catalyst, Policy
  Total Chron = minimum across all 5 dimensions.
  The sphere is only as alive as its weakest dimension.

Each dimension scores 0-100. Scoring is based on:
  - Which capabilities produced deliverables (primary drivers)
  - Which stages those deliverables came from (stage weight)
  - Body-of-work references (quality signal)
  - Unlikely collisions (innovation bonus)
  - Prior art usage (compounding bonus)
"""

from typing import Dict, List, Tuple
from models import GameType, ProductionStage


# ── Dimension definitions ───────────────────────────────────────

COSM_DIMENSIONS = {
    "rights": {
        "label": "Rights",
        "description": "How well did the team map and secure legal entitlements?",
        "primary_cap": "legal_navigation",
        "secondary_caps": ["data_systems"],
        "stage_weights": {
            "development": 25,       # map the landscape
            "pre_production": 20,     # blueprint coordination
            "production": 20,         # policy brief
            "post_production": 20,    # stress test
            "distribution": 15,       # publish
        },
    },
    "research": {
        "label": "Research",
        "description": "How thorough is the systems analysis and data modeling?",
        "primary_cap": "data_systems",
        "secondary_caps": ["flourishing_design"],
        "stage_weights": {
            "development": 30,
            "pre_production": 25,
            "production": 15,
            "post_production": 20,
            "distribution": 10,
        },
    },
    "budget": {
        "label": "Budget",
        "description": "How viable is the financial model and coordination economics?",
        "primary_cap": "data_systems",
        "secondary_caps": ["legal_navigation"],
        "stage_weights": {
            "development": 10,
            "pre_production": 30,
            "production": 30,
            "post_production": 20,
            "distribution": 10,
        },
    },
    "package": {
        "label": "Package",
        "description": "How complete is the dome design and does it produce awe? "
                        "A dome that documents everything but moves no one is incomplete.",
        "primary_cap": "flourishing_design",
        "secondary_caps": ["legal_navigation", "data_systems"],
        "awe_weighted": True,  # Dome awe design boosts this dimension
        "stage_weights": {
            "development": 15,
            "pre_production": 20,
            "production": 30,
            "post_production": 25,
            "distribution": 10,
        },
    },
    "deliverables": {
        "label": "Deliverables",
        "description": "Volume and quality of production outputs across all capabilities.",
        "primary_cap": None,  # all capabilities contribute equally
        "secondary_caps": [],
        "stage_weights": {
            "development": 15,
            "pre_production": 20,
            "production": 30,
            "post_production": 20,
            "distribution": 15,
        },
    },
    "pitch": {
        "label": "Pitch",
        "description": "How compelling is the narrative and publication package?",
        "primary_cap": "narrative",
        "secondary_caps": ["flourishing_design"],
        "stage_weights": {
            "development": 15,
            "pre_production": 15,
            "production": 25,
            "post_production": 20,
            "distribution": 25,
        },
    },
}

CHRON_DIMENSIONS = {
    "unlock": {
        "label": "Unlock",
        "description": "How well did the team navigate zoning, permits, and regulatory landscape?",
        "primary_cap": "spatial_legal",
        "secondary_caps": ["economics"],
        "stage_weights": {
            "development": 30,
            "pre_production": 25,
            "production": 20,
            "post_production": 15,
            "distribution": 10,
        },
    },
    "access": {
        "label": "Access",
        "description": "How accessible is the activation and how much awe does it produce? "
                        "A space that produces measurable awe scores higher — public space "
                        "activation without awe is just programming.",
        "primary_cap": "activation_design",
        "secondary_caps": ["narrative"],
        "awe_weighted": True,  # Awe metrics boost this dimension
        "stage_weights": {
            "development": 15,
            "pre_production": 25,
            "production": 30,
            "post_production": 20,
            "distribution": 10,
        },
    },
    "permanence": {
        "label": "Permanence",
        "description": "How sustainable is the activation over time?",
        "primary_cap": "economics",
        "secondary_caps": ["spatial_legal", "activation_design"],
        "stage_weights": {
            "development": 10,
            "pre_production": 15,
            "production": 25,
            "post_production": 30,
            "distribution": 20,
        },
    },
    "catalyst": {
        "label": "Catalyst",
        "description": "How much economic and social catalyst does the activation create?",
        "primary_cap": "economics",
        "secondary_caps": ["activation_design"],
        "stage_weights": {
            "development": 15,
            "pre_production": 20,
            "production": 30,
            "post_production": 25,
            "distribution": 10,
        },
    },
    "policy": {
        "label": "Policy",
        "description": "How replicable is the activation model? Does it generate policy?",
        "primary_cap": "spatial_legal",
        "secondary_caps": ["narrative", "economics"],
        "stage_weights": {
            "development": 10,
            "pre_production": 15,
            "production": 15,
            "post_production": 25,
            "distribution": 35,
        },
    },
}


# ── Scoring engine ──────────────────────────────────────────────

def score_dimensions(
    game_type: GameType,
    stage_log: List[Dict],
) -> Dict:
    """
    Score a production across all dimensions based on its stage log.
    Returns dimension scores, total score, and breakdown.
    """
    dims = COSM_DIMENSIONS if game_type == GameType.DOMES else CHRON_DIMENSIONS
    score_name = "cosm" if game_type == GameType.DOMES else "chron"

    dim_scores = {}
    dim_details = {}

    for dim_key, dim_def in dims.items():
        raw = 0.0
        detail_parts = []
        has_awe_content = False

        for entry in stage_log:
            stage_key = entry.get("stage", "")
            stage_weight = dim_def["stage_weights"].get(stage_key, 0)
            if stage_weight == 0:
                continue

            # Count deliverables that contribute to this dimension
            stage_contribution = 0.0

            for d in entry.get("deliverables", []):
                cap = d.get("capability", "")
                # Strip "unlikely:" prefix for matching
                clean_cap = cap.replace("unlikely:", "")

                is_primary = (dim_def["primary_cap"] is None or
                              clean_cap == dim_def["primary_cap"])
                is_secondary = clean_cap in dim_def["secondary_caps"]
                is_unlikely = d.get("is_unlikely", False)

                if dim_def["primary_cap"] is None:
                    # "deliverables" dimension: all caps contribute equally
                    contrib = 1.0
                elif is_primary:
                    contrib = 1.0
                elif is_secondary:
                    contrib = 0.4
                elif is_unlikely:
                    contrib = 0.3  # unlikely collisions help all dimensions a bit
                else:
                    contrib = 0.0

                if contrib <= 0:
                    continue

                # Base deliverable score
                del_score = 12.0 * contrib

                # Body-of-work reference bonus
                work_refs = d.get("work_referenced", [])
                if work_refs:
                    del_score += 4.0 * min(len(work_refs), 3) * contrib

                # Prior art bonus
                if d.get("built_on"):
                    del_score += 5.0 * contrib

                # Unlikely collision bonus
                if is_unlikely:
                    del_score += 8.0

                # Awe design bonus: deliverables that include awe trigger
                # documentation score higher on awe-weighted dimensions
                if dim_def.get("awe_weighted"):
                    desc = d.get("description", "").lower()
                    awe_signals = ["awe_s", "awe-s", "awe trigger", "keltner",
                                   "vastness", "accommodation", "collective effervescence",
                                   "moral beauty", "prosocial", "time expansion",
                                   "piloerection", "vagal tone", "hrv"]
                    awe_hits = sum(1 for sig in awe_signals if sig in desc)
                    if awe_hits >= 3:
                        del_score += 10.0 * contrib  # Significant awe design bonus
                        has_awe_content = True
                    elif awe_hits >= 1:
                        del_score += 4.0 * contrib   # Partial awe awareness
                        has_awe_content = True

                stage_contribution += del_score

            # Apply stage weight (percentage of what this stage can contribute)
            weighted = stage_contribution * (stage_weight / 100.0)
            raw += weighted

            if stage_contribution > 0:
                detail_parts.append({
                    "stage": stage_key,
                    "raw_contribution": round(stage_contribution, 1),
                    "weight": stage_weight,
                    "weighted": round(weighted, 1),
                })

        # Normalize: a perfect single-stage contribution is ~24 points raw,
        # across 5 stages with full coverage = ~120 raw → map to 0-100
        normalized = min(round(raw * 0.85, 1), 100.0)

        dim_scores[dim_key] = normalized
        dim_details[dim_key] = {
            "label": dim_def["label"],
            "description": dim_def["description"],
            "score": normalized,
            "breakdown": detail_parts,
        }

    # Total = minimum across all dimensions
    total = min(dim_scores.values()) if dim_scores else 0.0

    return {
        "score_type": score_name,
        "total": round(total, 1),
        "dimensions": dim_scores,
        "dimension_details": dim_details,
        "weakest": min(dim_scores, key=dim_scores.get) if dim_scores else None,
        "strongest": max(dim_scores, key=dim_scores.get) if dim_scores else None,
    }


def score_stage_live(
    game_type: GameType,
    stage_log: List[Dict],
) -> Dict:
    """
    Compute live dimension scores after each stage for progressive display.
    Returns the full dimension breakdown plus per-stage deltas.
    """
    result = score_dimensions(game_type, stage_log)

    # Also compute what changed at the last stage
    if len(stage_log) > 1:
        prev = score_dimensions(game_type, stage_log[:-1])
        deltas = {}
        for dim_key in result["dimensions"]:
            deltas[dim_key] = round(
                result["dimensions"][dim_key] - prev["dimensions"].get(dim_key, 0), 1
            )
        result["stage_deltas"] = deltas
        result["total_delta"] = round(result["total"] - prev["total"], 1)
    else:
        result["stage_deltas"] = {k: v for k, v in result["dimensions"].items()}
        result["total_delta"] = result["total"]

    return result
