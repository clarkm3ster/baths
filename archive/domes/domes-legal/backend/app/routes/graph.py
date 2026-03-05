"""Graph routes — provision relationship queries."""
import json
import math
from collections import defaultdict
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from ..database import get_db
from ..models import Provision, ProvisionRelationship

router = APIRouter(prefix="/api/graph", tags=["graph"])

DOMAIN_COLORS = {
    "health": "#1A6B3C", "justice": "#8B1A1A", "housing": "#1A3D8B",
    "income": "#6B5A1A", "education": "#5A1A6B", "child_welfare": "#1A6B6B",
    "civil_rights": "#6B1A4B",
}


def _provision_to_node(p, x=0, y=0):
    return {
        "id": p.id, "citation": p.citation, "title": p.title,
        "domain": p.domain, "type": p.provision_type,
        "color": DOMAIN_COLORS.get(p.domain, "#333"), "x": x, "y": y,
    }


def _rel_to_edge(r):
    return {
        "source": r.source_id, "target": r.target_id,
        "type": r.relationship_type,
        "label": r.description or r.relationship_type,
        "confidence": r.confidence,
    }


def _layout_nodes(nodes):
    """Simple domain-clustered layout."""
    domain_groups = defaultdict(list)
    for n in nodes:
        domain_groups[n["domain"]].append(n)
    domains = list(domain_groups.keys())
    for i, domain in enumerate(domains):
        angle = (2 * math.pi * i) / max(len(domains), 1)
        cx = 400 + 250 * math.cos(angle)
        cy = 300 + 200 * math.sin(angle)
        group = domain_groups[domain]
        for j, node in enumerate(group):
            sub_angle = (2 * math.pi * j) / max(len(group), 1)
            node["x"] = round(cx + 80 * math.cos(sub_angle))
            node["y"] = round(cy + 80 * math.sin(sub_angle))
    return nodes


@router.get("/provision/{provision_id}")
def get_provision_graph(provision_id: int, depth: int = 2, db: Session = Depends(get_db)):
    """BFS graph from a provision."""
    visited = set()
    queue = [provision_id]
    nodes = {}
    edges = []
    for _ in range(depth):
        next_queue = []
        for pid in queue:
            if pid in visited:
                continue
            visited.add(pid)
            p = db.query(Provision).filter(Provision.id == pid).first()
            if p:
                nodes[pid] = _provision_to_node(p)
            rels = db.query(ProvisionRelationship).filter(
                or_(ProvisionRelationship.source_id == pid, ProvisionRelationship.target_id == pid)
            ).all()
            for r in rels:
                edges.append(_rel_to_edge(r))
                neighbor = r.target_id if r.source_id == pid else r.source_id
                if neighbor not in visited:
                    next_queue.append(neighbor)
                    np = db.query(Provision).filter(Provision.id == neighbor).first()
                    if np:
                        nodes[neighbor] = _provision_to_node(np)
        queue = next_queue
    node_list = _layout_nodes(list(nodes.values()))
    seen_edges = set()
    unique_edges = []
    for e in edges:
        key = (e["source"], e["target"], e["type"])
        if key not in seen_edges:
            seen_edges.add(key)
            unique_edges.append(e)
    return {"nodes": node_list, "edges": unique_edges}


@router.get("/provision/{provision_id}/chain")
def get_chain(provision_id: int, db: Session = Depends(get_db)):
    """Follow the chain: right -> obligation -> enforcement."""
    visited = set()
    chain = []
    current = provision_id
    for _ in range(10):
        if current in visited:
            break
        visited.add(current)
        p = db.query(Provision).filter(Provision.id == current).first()
        if not p:
            break
        rels = db.query(ProvisionRelationship).filter(
            ProvisionRelationship.source_id == current
        ).all()
        chain.append({"provision": _provision_to_node(p), "relationships": [_rel_to_edge(r) for r in rels]})
        # Follow first enforcement or implements link
        next_rel = next((r for r in rels if r.relationship_type in ("enforces", "implements", "triggers")), None)
        if next_rel:
            current = next_rel.target_id
        else:
            break
    return chain


@router.get("/provision/{provision_id}/neighbors")
def get_neighbors(provision_id: int, db: Session = Depends(get_db)):
    rels = db.query(ProvisionRelationship).filter(
        or_(ProvisionRelationship.source_id == provision_id, ProvisionRelationship.target_id == provision_id)
    ).all()
    neighbor_ids = set()
    edges = []
    for r in rels:
        edges.append(_rel_to_edge(r))
        neighbor_ids.add(r.target_id if r.source_id == provision_id else r.source_id)
    neighbors = db.query(Provision).filter(Provision.id.in_(neighbor_ids)).all()
    return {
        "center": provision_id,
        "neighbors": [_provision_to_node(n) for n in neighbors],
        "edges": edges,
    }


@router.get("/path")
def find_path(source: int, target: int, db: Session = Depends(get_db)):
    """BFS shortest path."""
    if source == target:
        return {"path": [source], "edges": []}
    visited = {source}
    queue = [(source, [source])]
    path_edges = []
    while queue:
        current, path = queue.pop(0)
        rels = db.query(ProvisionRelationship).filter(
            or_(ProvisionRelationship.source_id == current, ProvisionRelationship.target_id == current)
        ).all()
        for r in rels:
            neighbor = r.target_id if r.source_id == current else r.source_id
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                if neighbor == target:
                    provisions = db.query(Provision).filter(Provision.id.in_(new_path)).all()
                    prov_map = {p.id: p for p in provisions}
                    return {
                        "path": [_provision_to_node(prov_map[pid]) for pid in new_path if pid in prov_map],
                        "length": len(new_path) - 1,
                    }
                queue.append((neighbor, new_path))
    return {"path": [], "length": -1, "message": "No path found"}


@router.post("/build")
def build_relationships(db: Session = Depends(get_db)):
    """Auto-detect relationships from cross-references."""
    provisions = db.query(Provision).all()
    cite_map = {p.citation: p.id for p in provisions}
    added = 0
    for p in provisions:
        xrefs = json.loads(p.cross_references or "[]")
        for ref in xrefs:
            target_id = cite_map.get(ref)
            if target_id and target_id != p.id:
                existing = db.query(ProvisionRelationship).filter(
                    ProvisionRelationship.source_id == p.id,
                    ProvisionRelationship.target_id == target_id,
                ).first()
                if not existing:
                    db.add(ProvisionRelationship(
                        source_id=p.id, target_id=target_id,
                        relationship_type="cross_references",
                        description=f"{p.citation} references {ref}",
                        confidence=0.9,
                    ))
                    added += 1
    db.commit()
    return {"added": added}


@router.get("/stats")
def graph_stats(db: Session = Depends(get_db)):
    node_count = db.query(Provision).filter(Provision.is_current == True).count()
    edge_count = db.query(ProvisionRelationship).count()
    type_dist = dict(
        db.query(ProvisionRelationship.relationship_type, func.count(ProvisionRelationship.id))
        .group_by(ProvisionRelationship.relationship_type).all()
    )
    return {"nodes": node_count, "edges": edge_count, "relationship_types": type_dist}


@router.get("/full")
def full_graph(domain: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Provision).filter(Provision.is_current == True)
    if domain:
        query = query.filter(Provision.domain == domain)
    provisions = query.all()
    prov_ids = {p.id for p in provisions}
    nodes = [_provision_to_node(p) for p in provisions]
    all_rels = db.query(ProvisionRelationship).all()
    edges = [_rel_to_edge(r) for r in all_rels if r.source_id in prov_ids or r.target_id in prov_ids]
    nodes = _layout_nodes(nodes)
    return {"nodes": nodes, "edges": edges}
