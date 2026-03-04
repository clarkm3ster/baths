"""FastAPI routes for the Material Orchestration layer.

REST endpoints for material state management and a WebSocket endpoint
for real-time 10Hz state streaming.
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from src.materials.orchestrator import MaterialOrchestrator

router = APIRouter()

# In-memory orchestrator registry (keyed by sphere_id)
_orchestrators: dict[str, MaterialOrchestrator] = {}


def _get_or_create_orchestrator(
    sphere_id: str,
    material_inventory: list[str] | None = None,
) -> MaterialOrchestrator:
    """Get or create an orchestrator for a sphere."""
    if sphere_id not in _orchestrators:
        inventory = material_inventory or [
            "acoustic_metamaterial",
            "electrochromic_surface",
            "projection_mapping",
            "haptic_surface",
            "olfactory_synthesis",
            "phase_change_panel",
        ]
        _orchestrators[sphere_id] = MaterialOrchestrator(
            sphere_id=uuid.UUID(sphere_id),
            material_inventory=inventory,
            simulation_speed=0.001,
        )
    return _orchestrators[sphere_id]


class MaterialCommandRequest(BaseModel):
    system_type: str
    config: dict[str, Any]


class MaterialConfigRequest(BaseModel):
    config: dict[str, Any]
    transition_plan: list[str] | None = None


@router.get("/spheres/{sphere_id}/material-state")
async def get_material_state(sphere_id: str) -> dict[str, Any]:
    """Get current state snapshot of all material systems."""
    orchestrator = _get_or_create_orchestrator(sphere_id)
    state = await orchestrator.read_all_states()
    return {
        "sphere_id": sphere_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "material_state": state,
    }


@router.post("/spheres/{sphere_id}/material-command")
async def send_material_command(
    sphere_id: str,
    req: MaterialCommandRequest,
) -> dict[str, Any]:
    """Send a direct command to a specific material driver."""
    orchestrator = _get_or_create_orchestrator(sphere_id)
    from src.materials.drivers.base import MaterialSystemType

    try:
        system_type = MaterialSystemType(req.system_type)
    except ValueError:
        return {"success": False, "error": f"Unknown system: {req.system_type}"}

    driver = orchestrator.drivers.get(system_type)
    if not driver:
        return {"success": False, "error": f"System not installed: {req.system_type}"}

    response = await driver.apply_config(req.config)
    return response.model_dump()


@router.post("/spheres/{sphere_id}/material-config")
async def apply_material_config(
    sphere_id: str,
    req: MaterialConfigRequest,
) -> dict[str, Any]:
    """Apply a full MaterialConfiguration to a Sphere."""
    orchestrator = _get_or_create_orchestrator(sphere_id)
    try:
        responses = await orchestrator.apply_configuration(
            target=req.config,
            transition_plan=req.transition_plan,
        )
        return {
            "success": True,
            "responses": {k: v.model_dump() for k, v in responses.items()},
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/spheres/{sphere_id}/emergency-reset")
async def emergency_reset(sphere_id: str) -> dict[str, str]:
    """Trigger emergency reset on all material drivers."""
    orchestrator = _get_or_create_orchestrator(sphere_id)
    await orchestrator.emergency_reset_all()
    return {"status": "reset_complete", "sphere_id": sphere_id}


@router.get("/materials/drivers")
async def list_drivers() -> list[dict[str, Any]]:
    """List available material driver types with TRL info."""
    from src.materials.drivers import DRIVER_REGISTRY
    result = []
    for system_type, driver_cls in DRIVER_REGISTRY.items():
        driver = driver_cls(simulation_speed=0.001)
        result.append(driver.info().model_dump())
    return result


@router.websocket("/spheres/{sphere_id}/material-stream")
async def material_stream(websocket: WebSocket, sphere_id: str) -> None:
    """Real-time material state updates at 10Hz via WebSocket."""
    await websocket.accept()
    orchestrator = _get_or_create_orchestrator(sphere_id)

    try:
        while True:
            state = await orchestrator.read_all_states()
            await websocket.send_json({
                "sphere_id": sphere_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "material_state": state,
            })
            await asyncio.sleep(0.1)  # 10Hz
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
