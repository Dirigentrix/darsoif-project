import json
import os
from enum import Enum
from typing import Dict, Any, List

class Mode(Enum):
    OFFLINE = "OFFLINE"
    LIMITED = "LIMITED"
    FULL = "FULL"

class CoreGeometry:
    def __init__(self):
        self.dimensions = (40, 40)
        self.vectors = []

class StateEngine:
    def __init__(self, mode: Mode = Mode.OFFLINE):
        self.mode = mode
        self.history = []

    def set_mode(self, mode: Mode):
        self.mode = mode

class LedgerPassportos:
    def __init__(self):
        self.entries = {}

    def log_decision(self, sensor_id: str, decision: str):
        self.entries[sensor_id] = decision
        self._write_to_log(sensor_id, decision)

    def _write_to_log(self, sensor_id: str, decision: str):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, "gateway_events.jsonl")
        event = {"sensor_id": sensor_id, "decision": decision}
        with open(log_file, "a") as f:
            f.write(json.dumps(event) + "\n")

class AgentLeon:
    def decide_qwen(self, sensor_data: Dict[str, Any]) -> str:
        """Adapter for AgentLeon routing in FULL mode."""
        return "QWEN_DECISION_PLACEHOLDER"

class Kernel:
    def reguly_40x40(self, sensor_data: Dict[str, Any]) -> str:
        """Kernel logic for offline/limited fallback."""
        # Spec logic: Example returns WATER for high moisture
        moisture = sensor_data.get("moisture", 0.0)
        if moisture > 0.5:
            return "WATER"
        return "DRY"

class DARSOIF:
    """
    DARSOIF System Implementation
    Architecture: CoreGeometry, StateEngine, LedgerPassportos, AgentLeon.
    """
    def __init__(self):
        self.geometry = CoreGeometry()
        self.state = StateEngine()
        self.ledger = LedgerPassportos()
        self.leon = AgentLeon()
        self.kernel = Kernel()

    def darsoif_decide(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        sensor_id = str(sensor_data.get("id", "unknown"))
        
        # Logic routing based on system mode
        if self.state.mode in [Mode.OFFLINE, Mode.LIMITED]:
            decision = self.kernel.reguly_40x40(sensor_data)
        else:
            decision = self.leon.decide_qwen(sensor_data)
            
        self.ledger.log_decision(sensor_id, decision)
        
        return {
            "sensor_id": sensor_id,
            "decision": decision,
            "mode": self.state.mode.value
        }

# Global system instance
darsoif_system = DARSOIF()

def darsoif_decide(sensor_data: Dict[str, Any]) -> Dict[str, Any]:
    """Primary entry point for decisions."""
    return darsoif_system.darsoif_decide(sensor_data)

if __name__ == "__main__":
    # Internal Demo/Test Path
    print("--- DARSOIF System Demo ---")
    test_input = {"id": "S_001", "moisture": 0.8}
    print(f"Input: {test_input}")
    print(f"Mode: {darsoif_system.state.mode.value}")
    result = darsoif_decide(test_input)
    print(f"Result: {result}")
    
    # Assert for demo sanity
    assert result["decision"] == "WATER", "Offline WATER test failed"
    print("Demo: Offline WATER test passed.")
