import numpy as np
from typing import Dict, Any

class DartrixEquation:
    """
    Implements the fundamental Dartrix growth dynamics.
    
    Formula: Logistic Growth with Rotational Torsion
    L(t) = K / (1 + exp(-r(t-t0)))
    R(t) = A * sin(omega * t + phi) * exp(alpha * t)
    """

    def __init__(self, K: float = 1.0, r: float = 0.1, t0: float = 0.0):
        self.K = K  # Carrying capacity
        self.r = r  # Growth rate
        self.t0 = t0 # Sigmoid midpoint

    def compute_logistic(self, t: np.ndarray) -> np.ndarray:
        """Calculates the baseline logistic curve."""
        return self.K / (1 + np.exp(-self.r * (t - self.t0)))

    def compute_spiral(self, t: np.ndarray, omega: float = 1.0, alpha: float = 0.05) -> np.ndarray:
        """Calculates the rotational component (spiral growth)."""
        return np.exp(alpha * t) * np.cos(omega * t)

    def apply_saturation(self, x: np.ndarray) -> np.ndarray:
        """Applies tanh saturation for signal bounding."""
        return np.tanh(x)

    def get_state(self, t: float) -> Dict[str, float]:
        t_val = np.array([t])
        growth = self.compute_logistic(t_val)[0]
        spiral = self.compute_spiral(t_val)[0]
        combined = self.apply_saturation(growth * spiral)
        return {
            "t": t,
            "growth": growth,
            "spiral": spiral,
            "combined": combined
        }
