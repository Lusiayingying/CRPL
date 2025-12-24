"""
CRPL Core Rhythm Detector

This module contains the main RhythmDetector class that captures and analyzes
keystroke rhythm patterns to infer cognitive and emotional states.

Copyright (c) 2025 Yingying Chen & Anran Lin
"""

import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from math import sqrt

from .types import TypingEvent, RhythmType, FluencyLevel, PausePattern


class RhythmDetector:
    """
    Main class for detecting and analyzing keystroke rhythm patterns.
    
    Captures 24 fine-grained behavioral features organized into 7 categories:
    - Baseline Metrics (7 fields)
    - Basic Statistics (3 fields)
    - Deletion Analysis (3 fields)
    - Modification Analysis (2 fields)
    - Burst Detection (3 fields)
    - Hesitation Mapping (3 fields)
    - Fluency Scoring (2 fields)
    - Trajectory Recording (1 field)
    
    Example:
        detector = RhythmDetector()
        detector.start_monitoring()
        
        # Record keystrokes from your input handler
        detector.record_keystroke('H', 'type')
        detector.record_keystroke('i', 'type')
        
        # Get analysis
        results = detector.finish_monitoring("Hi")
        print(results['rhythm_type'])  # e.g., 'fluid'
    """
    
    # Configurable thresholds
    SHORT_PAUSE_MIN = 2.0      # seconds
    SHORT_PAUSE_MAX = 5.0      # seconds
    MEDIUM_PAUSE_MIN = 5.0     # seconds
    MEDIUM_PAUSE_MAX = 15.0    # seconds
    LONG_PAUSE_MIN = 15.0      # seconds
    
    HESITATION_THRESHOLD = 3.0  # seconds
    BURST_INTERVAL_MAX = 0.15   # seconds (150ms)
    BURST_MIN_LENGTH = 5        # keystrokes
    
    def __init__(self):
        """Initialize the rhythm detector."""
        self.events: List[TypingEvent] = []
        self.is_monitoring: bool = False
        self.start_time: Optional[float] = None
        
    def start_monitoring(self) -> None:
        """
        Begin keystroke monitoring session.
        
        Resets all state and starts fresh recording.
        """
        self.events = []
        self.is_monitoring = True
        self.start_time = time.time()
        
    def record_keystroke(self, char: str = "", event_type: str = "type") -> None:
        """
        Record a single keystroke event.
        
        Args:
            char: The character typed (empty string for deletions)
            event_type: One of "type", "backspace", "delete", "selection"
            
        Note:
            For Chinese IME input, record both Pinyin keystrokes and 
            final character selections for accurate rhythm analysis.
        """
        if not self.is_monitoring:
            return
            
        event = TypingEvent(
            event_type=event_type,
            char=char,
            timestamp=time.time()
        )
        self.events.append(event)
        
    def finish_monitoring(self, final_text: str) -> Dict[str, Any]:
        """
        Complete monitoring and return comprehensive 24-field analysis.
        
        Args:
            final_text: The final text content after all edits
            
        Returns:
            Dictionary containing all 24 rhythm analysis fields
        """
        self.is_monitoring = False
        end_time = time.time()
        
        if not self.events or not self.start_time:
            return self._empty_result()
            
        return self._analyze(final_text, end_time)
        
    def _analyze(self, final_text: str, end_time: float) -> Dict[str, Any]:
        """Perform full rhythm analysis."""
        
        # Calculate basic metrics
        duration = end_time - self.start_time
        total_keystrokes = len(self.events)
        actual_chars = len(final_text)
        
        # Filter typing events for interval calculation
        type_events = [e for e in self.events 
                       if e.event_type in ('type', 'composition', 'composition_confirm')]
        
        # Calculate intervals
        intervals = []
        for i in range(1, len(type_events)):
            interval = type_events[i].timestamp - type_events[i-1].timestamp
            intervals.append(interval)
            
        # Average interval
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        
        # Characters per minute
        cpm = (actual_chars / duration * 60) if duration > 0 else 0
        
        # Consistency (coefficient of variation based)
        consistency = self._calculate_consistency(intervals)
        
        # Pause analysis
        pause_pattern = self._analyze_pauses(intervals)
        
        # Deletion analysis
        deletion_count, deletion_ratio, deletion_patterns = self._analyze_deletions()
        
        # Modification analysis
        modification_count, modifications = self._analyze_modifications()
        
        # Burst detection
        burst_count, burst_segments, max_burst_speed = self._detect_bursts(intervals)
        
        # Hesitation mapping
        hesitation_count, hesitation_locations, hesitations = self._map_hesitations(intervals)
        
        # Fluency scoring
        fluency_score, fluency_level = self._calculate_fluency(
            consistency, deletion_ratio, pause_pattern, hesitation_count
        )
        
        # Rhythm type classification
        rhythm_type = self._classify_rhythm_type(
            cpm, consistency, pause_pattern['pattern']
        )
        
        # Text rhythm analysis
        text_rhythm = self._analyze_text_rhythm(final_text)
        
        # Keystroke ratio (important for Chinese IME)
        keystroke_ratio = total_keystrokes / actual_chars if actual_chars > 0 else 0
        
        return {
            # Baseline Metrics (7)
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(duration, 2),
            "chars_per_minute": round(cpm, 1),
            "pause_pattern": pause_pattern,
            "consistency": round(consistency, 3),
            "text_rhythm": text_rhythm,
            "rhythm_type": rhythm_type,
            
            # Basic Statistics (3)
            "total_keystrokes": total_keystrokes,
            "actual_chars": actual_chars,
            "avg_interval": round(avg_interval, 3),
            
            # Deletion Analysis (3)
            "deletion_count": deletion_count,
            "deletion_ratio": round(deletion_ratio, 3),
            "deletion_patterns": deletion_patterns,
            
            # Modification Analysis (2)
            "modification_count": modification_count,
            "modifications": modifications,
            
            # Burst Detection (3)
            "burst_count": burst_count,
            "burst_segments": burst_segments,
            "max_burst_speed": round(max_burst_speed, 1),
            
            # Hesitation Mapping (3)
            "hesitation_count": hesitation_count,
            "hesitation_locations": hesitation_locations,
            "hesitations": hesitations,
            
            # Fluency Scoring (2)
            "fluency_score": round(fluency_score, 3),
            "fluency_level": fluency_level,
            
            # Trajectory Recording (1)
            "typing_trajectory": [
                {"type": e.event_type, "char": e.char, "time": e.timestamp}
                for e in self.events
            ],
            
            # Additional metrics
            "keystroke_ratio": round(keystroke_ratio, 2)
        }
        
    def _calculate_consistency(self, intervals: List[float]) -> float:
        """Calculate rhythm consistency using coefficient of variation."""
        if len(intervals) < 2:
            return 0.0
            
        mean = sum(intervals) / len(intervals)
        if mean == 0:
            return 0.0
            
        variance = sum((x - mean) ** 2 for x in intervals) / len(intervals)
        std_dev = sqrt(variance)
        cv = std_dev / mean
        
        # Convert CV to 0-1 consistency score (lower CV = higher consistency)
        return max(0.0, min(1.0, 1 - cv / 2))
        
    def _analyze_pauses(self, intervals: List[float]) -> Dict[str, Any]:
        """Analyze pause patterns in typing."""
        short_pauses = sum(1 for i in intervals 
                          if self.SHORT_PAUSE_MIN <= i < self.SHORT_PAUSE_MAX)
        medium_pauses = sum(1 for i in intervals 
                           if self.MEDIUM_PAUSE_MIN <= i < self.MEDIUM_PAUSE_MAX)
        long_pauses = sum(1 for i in intervals 
                         if i >= self.LONG_PAUSE_MIN)
        
        # Determine pattern
        if long_pauses > 0:
            pattern = PausePattern.CONTEMPLATIVE
        elif medium_pauses > 0:
            pattern = PausePattern.THOUGHTFUL
        elif short_pauses > 0:
            pattern = PausePattern.CHOPPY
        else:
            pattern = PausePattern.CONTINUOUS
            
        return {
            "short_pauses": short_pauses,
            "medium_pauses": medium_pauses,
            "long_pauses": long_pauses,
            "pattern": pattern.value
        }
        
    def _analyze_deletions(self) -> tuple:
        """Analyze deletion behavior."""
        deletion_events = [e for e in self.events 
                          if e.event_type in ('backspace', 'delete', 'composition_delete')]
        deletion_count = len(deletion_events)
        deletion_ratio = deletion_count / len(self.events) if self.events else 0
        
        # Detect deletion patterns (consecutive deletions, etc.)
        patterns = []
        consecutive = 0
        for e in self.events:
            if e.event_type in ('backspace', 'delete'):
                consecutive += 1
            else:
                if consecutive >= 3:
                    patterns.append({
                        "type": "consecutive",
                        "length": consecutive
                    })
                consecutive = 0
                
        return deletion_count, deletion_ratio, patterns
        
    def _analyze_modifications(self) -> tuple:
        """Analyze text modification behavior."""
        # Simplified: count selection events as modifications
        mod_events = [e for e in self.events if e.event_type == 'selection']
        return len(mod_events), []
        
    def _detect_bursts(self, intervals: List[float]) -> tuple:
        """Detect burst typing segments."""
        bursts = []
        current_burst_length = 0
        current_burst_time = 0
        burst_start = 0
        
        for i, interval in enumerate(intervals):
            if interval < self.BURST_INTERVAL_MAX:
                if current_burst_length == 0:
                    burst_start = i
                current_burst_length += 1
                current_burst_time += interval
            else:
                if current_burst_length >= self.BURST_MIN_LENGTH:
                    avg_speed = current_burst_length / current_burst_time if current_burst_time > 0 else 0
                    bursts.append({
                        "start": burst_start,
                        "length": current_burst_length,
                        "avg_speed": round(avg_speed, 1)
                    })
                current_burst_length = 0
                current_burst_time = 0
                
        # Check final burst
        if current_burst_length >= self.BURST_MIN_LENGTH:
            avg_speed = current_burst_length / current_burst_time if current_burst_time > 0 else 0
            bursts.append({
                "start": burst_start,
                "length": current_burst_length,
                "avg_speed": round(avg_speed, 1)
            })
            
        max_speed = max((b["avg_speed"] for b in bursts), default=0)
        return len(bursts), bursts, max_speed
        
    def _map_hesitations(self, intervals: List[float]) -> tuple:
        """Map hesitation points in typing."""
        hesitations = []
        locations = []
        
        for i, interval in enumerate(intervals):
            if interval >= self.HESITATION_THRESHOLD:
                locations.append(i)
                
                # Determine severity
                if interval >= 10:
                    severity = "very_long"
                elif interval >= 5:
                    severity = "long"
                else:
                    severity = "medium"
                    
                hesitations.append({
                    "location": i,
                    "duration": round(interval, 2),
                    "severity": severity
                })
                
        return len(hesitations), locations, hesitations
        
    def _calculate_fluency(self, consistency: float, deletion_ratio: float,
                          pause_pattern: Dict, hesitation_count: int) -> tuple:
        """Calculate composite fluency score."""
        # Stability component (30%)
        stability_score = consistency
        
        # Deletion component (30%)
        deletion_score = max(0, 1 - deletion_ratio * 2)
        
        # Pause component (20%)
        pause_penalty = (pause_pattern["short_pauses"] + 
                        pause_pattern["medium_pauses"] * 2 + 
                        pause_pattern["long_pauses"] * 3) / 10
        pause_score = max(0, 1 - pause_penalty)
        
        # Hesitation component (20%)
        hesitation_score = max(0, 1 - hesitation_count / 5)
        
        # Weighted combination
        fluency_score = (0.30 * stability_score +
                        0.30 * deletion_score +
                        0.20 * pause_score +
                        0.20 * hesitation_score)
        
        # Determine level
        if fluency_score >= 0.8:
            level = FluencyLevel.VERY_FLUENT
        elif fluency_score >= 0.6:
            level = FluencyLevel.FLUENT
        elif fluency_score >= 0.4:
            level = FluencyLevel.NORMAL
        else:
            level = FluencyLevel.HESITANT
            
        return fluency_score, level.value
        
    def _classify_rhythm_type(self, cpm: float, consistency: float, 
                             pause_pattern: str) -> str:
        """Classify overall rhythm type."""
        # Fast typing (>120 CPM)
        if cpm > 120:
            if consistency > 0.7:
                return RhythmType.STEADY_FAST.value if pause_pattern == "continuous" else RhythmType.BURST_FAST.value
            else:
                return RhythmType.ERRATIC_FAST.value
                
        # Slow typing (<60 CPM)
        elif cpm < 60:
            if consistency > 0.7:
                return RhythmType.STEADY_SLOW.value
            else:
                if pause_pattern in ("thoughtful", "contemplative"):
                    return RhythmType.HESITANT.value
                else:
                    return RhythmType.LABORED.value
                    
        # Medium typing (60-120 CPM)
        else:
            if consistency > 0.7:
                return RhythmType.FLUID.value
            elif pause_pattern == "thoughtful":
                return RhythmType.MEASURED.value
            else:
                return RhythmType.UNEVEN.value
                
    def _analyze_text_rhythm(self, text: str) -> Dict[str, Any]:
        """Analyze text-level rhythm characteristics."""
        # Split into sentences
        import re
        sentences = re.split(r'[.!?。！？]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        sentence_count = len(sentences) or 1
        avg_sentence_length = len(text) / sentence_count
        
        # Punctuation density
        punctuation = re.findall(r'[.,!?;:，。！？；：～~]', text)
        punctuation_rate = len(punctuation) / len(text) if text else 0
        
        # Classify text rhythm
        if avg_sentence_length < 20 and punctuation_rate < 0.05:
            category = "concise"
        elif avg_sentence_length < 20 and punctuation_rate >= 0.05:
            category = "staccato"
        elif avg_sentence_length >= 50 and punctuation_rate < 0.05:
            category = "flowing"
        elif avg_sentence_length >= 50 and punctuation_rate >= 0.08:
            category = "complex"
        elif punctuation_rate >= 0.08:
            category = "punctuated"
        else:
            category = "balanced"
            
        return {
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "punctuation_rate": round(punctuation_rate, 3),
            "rhythm_category": category
        }
        
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result structure."""
        return {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": 0,
            "chars_per_minute": 0,
            "pause_pattern": {"short_pauses": 0, "medium_pauses": 0, "long_pauses": 0, "pattern": "continuous"},
            "consistency": 0,
            "text_rhythm": {"sentence_count": 0, "avg_sentence_length": 0, "punctuation_rate": 0, "rhythm_category": "balanced"},
            "rhythm_type": "balanced",
            "total_keystrokes": 0,
            "actual_chars": 0,
            "avg_interval": 0,
            "deletion_count": 0,
            "deletion_ratio": 0,
            "deletion_patterns": [],
            "modification_count": 0,
            "modifications": [],
            "burst_count": 0,
            "burst_segments": [],
            "max_burst_speed": 0,
            "hesitation_count": 0,
            "hesitation_locations": [],
            "hesitations": [],
            "fluency_score": 0,
            "fluency_level": "normal",
            "typing_trajectory": [],
            "keystroke_ratio": 0
        }
