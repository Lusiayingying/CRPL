"""
CRPL - Celestelin Rhythm Perception Layer

A fine-grained keystroke-rhythm perception framework for multi-agent cognition systems.

Copyright (c) 2025 Yingying Chen & Anran Lin
Licensed under MIT License
"""

from .detector import RhythmDetector
from .types import TypingEvent, RhythmType, FluencyLevel, PausePattern

__version__ = "1.0.0"
__author__ = "Yingying Chen & Anran Lin"
__all__ = [
    "RhythmDetector",
    "TypingEvent", 
    "RhythmType",
    "FluencyLevel",
    "PausePattern"
]
