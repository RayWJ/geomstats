"""
Cognitive Physics Engine (CPE) - Core Package

A prototype "World Simulator" that computes truth in curved space.
Combines Geomstats (Geometry) + PyTorch (Dynamics) + LLM (Semantics).
"""

__version__ = "0.1.0"
__author__ = "GeomStats AI Team"

from .manifold import CognitiveManifold
from .dynamics import CognitiveDynamics
from .translator import Translator
from .simulator import WorldSimulator

__all__ = [
    "CognitiveManifold",
    "CognitiveDynamics", 
    "Translator",
    "WorldSimulator",
]
