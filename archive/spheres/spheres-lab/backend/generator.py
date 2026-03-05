"""
SPHERES Innovation Laboratory — Random innovation generator.
Uses domain-specific templates to generate new innovations.
"""

import json
import random
from datetime import datetime, timezone

from models import Innovation, Teammate
from innovations import DOMAIN_TEMPLATES


def generate_innovation(db, slug: str) -> dict | None:
    """Generate a random innovation for the teammate with the given slug."""
    teammate = db.query(Teammate).filter_by(slug=slug).first()
    if not teammate:
        return None

    templates = DOMAIN_TEMPLATES.get(slug, [])
    if not templates:
        return None

    teammate.status = "generating"
    db.commit()

    template = random.choice(templates)

    impact = random.randint(template.get("impact_range", [3, 5])[0],
                            template.get("impact_range", [3, 5])[1])
    feasibility = random.randint(template.get("feasibility_range", [2, 4])[0],
                                 template.get("feasibility_range", [2, 4])[1])
    novelty = random.randint(template.get("novelty_range", [3, 5])[0],
                             template.get("novelty_range", [3, 5])[1])

    innovation = Innovation(
        teammate_id=teammate.id,
        title=template["title"],
        summary=template["summary"],
        domain=teammate.domain,
        category=template.get("category", "general"),
        impact_level=impact,
        feasibility=feasibility,
        novelty=novelty,
        time_horizon=template.get("time_horizon", "medium"),
        status="draft",
        details=json.dumps(template.get("details", {})),
        tags=",".join(template.get("tags", [])),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(innovation)
    teammate.status = "idle"
    db.commit()
    db.refresh(innovation)
    return innovation.to_dict()
