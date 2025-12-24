"""
CRPL Type Definitions

Data types and enumerations for the Rhythm Perception Layer.

Copyright (c) 2025 Yingying Chen & Anran Lin
"""

from dataclasses import dataclass
from enum import Enum


@dataclass
class TypingEvent:
    """
    Represents a single keystroke event.
    
    Attributes:
        event_type: Type of event ("type", "backspace", "delete", "selection",
                    "composition", "composition_delete", "composition_confirm")
        char: The character typed (empty for deletion events)
        timestamp: Unix timestamp with millisecond precision
    """
    event_type: str
    char: str
    timestamp: float


class RhythmType(Enum):
    """
    Classification of overall typing rhythm patterns.
    
    Each type maps to specific cognitive/emotional interpretations.
    """
    # Fast typing (>120 CPM)
    STEADY_FAST = "steady_fast"      # Confident, skilled
    BURST_FAST = "burst_fast"        # Inspired, energized
    ERRATIC_FAST = "erratic_fast"    # Agitated, rushed
    
    # Slow typing (<60 CPM)
    STEADY_SLOW = "steady_slow"      # Careful, deliberate
    HESITANT = "hesitant"            # Uncertain, exploring
    LABORED = "labored"              # Struggling, fatigued
    
    # Medium typing (60-120 CPM)
    FLUID = "fluid"                  # Flow state, natural
    MEASURED = "measured"            # Analytical, thoughtful
    UNEVEN = "uneven"                # Distracted, interrupted
    
    # Default
    BALANCED = "balanced"            # Neutral pattern


class FluencyLevel(Enum):
    """
    Categorical fluency levels based on composite scoring.
    """
    VERY_FLUENT = "very_fluent"  # Score >= 0.8
    FLUENT = "fluent"            # Score 0.6-0.8
    NORMAL = "normal"            # Score 0.4-0.6
    HESITANT = "hesitant"        # Score < 0.4


class PausePattern(Enum):
    """
    Classification of pause behavior patterns.
    """
    CONTINUOUS = "continuous"        # No significant pauses
    CHOPPY = "choppy"               # Mainly short pauses (2-5s)
    THOUGHTFUL = "thoughtful"       # Mainly medium pauses (5-15s)
    CONTEMPLATIVE = "contemplative" # Long pauses (>15s)
    MIXED = "mixed"                 # Mixed pattern


class HesitationSeverity(Enum):
    """
    Severity levels for hesitation events.
    """
    MEDIUM = "medium"       # 3-5 seconds
    LONG = "long"          # 5-10 seconds
    VERY_LONG = "very_long" # >10 seconds


# Cognitive interpretation mappings
RHYTHM_INTERPRETATIONS = {
    RhythmType.STEADY_FAST: "Confident expression, clear thinking, skilled typing",
    RhythmType.BURST_FAST: "Inspiration surge, emotional arousal, creative flow",
    RhythmType.ERRATIC_FAST: "Agitation, rushing, emotional turbulence",
    RhythmType.STEADY_SLOW: "Careful consideration, deliberate expression",
    RhythmType.HESITANT: "Uncertainty, exploration, searching for words",
    RhythmType.LABORED: "Difficulty, fatigue, cognitive strain",
    RhythmType.FLUID: "Flow state, natural expression, engaged focus",
    RhythmType.MEASURED: "Analytical thinking, careful word choice",
    RhythmType.UNEVEN: "Distraction, interruption, divided attention",
    RhythmType.BALANCED: "Neutral, baseline typing pattern"
}

PAUSE_INTERPRETATIONS = {
    PausePattern.CONTINUOUS: "Fluent thought flow, minimal cognitive interruption",
    PausePattern.CHOPPY: "Word-by-word consideration, careful expression",
    PausePattern.THOUGHTFUL: "Sentence-level planning, concept organization",
    PausePattern.CONTEMPLATIVE: "Deep reflection, complex decision-making",
    PausePattern.MIXED: "State fluctuation, multitasking interference"
}
