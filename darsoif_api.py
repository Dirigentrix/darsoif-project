from fastapi import FastAPI, Body
from typing import Dict, Any
from darsoif_core import darsoif_decide, darsoif_system, Mode

app = FastAPI(title="DARSOIF System API")

@app.post("/decide")
async def decide(sensor_data: Dict[str, Any] = Body(...)):
    """
    POST endpoint for Devvit/External sensor data.
    Returns the DARSOIF decision.
    """
    return darsoif_decide(sensor_data)

@app.get("/status")
async def status():
    """System status and geometry info."""
    return {
        "mode": darsoif_system.state.mode.value,
        "geometry": darsoif_system.geometry.dimensions,
        "ledger_count": len(darsoif_system.ledger.entries)
    }

@app.post("/mode")
async def set_mode(mode: str):
    """Change DARSOIF operational mode."""
    try:
        new_mode = Mode(mode.upper())
        darsoif_system.state.set_mode(new_mode)
        return {"status": "success", "new_mode": new_mode.value}
    except ValueError:
        return {"status": "error", "message": f"Invalid mode. Valid: {[m.value for m in Mode]}"}
