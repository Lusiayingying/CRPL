#!/usr/bin/env python3
"""
CRPL GUI Test Tool
💜 Standalone GUI for testing the Rhythm Detector

This tool can be run independently without CelestelinAgent.
Just make sure the 'crpl' folder is in the same directory.

Usage:
    python test_gui.py

Requirements:
    - Python 3.8+
    - tkinter (included in standard Python)

Author: Yingying Chen & Anran Lin
"""

import tkinter as tk
from tkinter import scrolledtext
import time
from datetime import datetime
from math import sqrt


class TypingEvent:
    """Single typing event"""
    def __init__(self, event_type: str, char: str, timestamp: float):
        self.event_type = event_type
        self.char = char
        self.timestamp = timestamp


class RhythmDetector:
    """
    Simplified Rhythm Detector for GUI testing.
    Captures all 24 fields for rhythm analysis.
    """
    
    def __init__(self):
        self.is_monitoring = False
        self.start_time = None
        self.events = []
    
    def start_monitoring(self):
        self.is_monitoring = True
        self.start_time = time.time()
        self.events = []
    
    def record_keystroke(self, char: str = "", event_type: str = "type"):
        if not self.is_monitoring:
            return
        self.events.append(TypingEvent(event_type, char, time.time()))
    
    def finish_monitoring(self, final_text: str) -> dict:
        if not self.is_monitoring:
            return {}
        
        end_time = time.time()
        self.is_monitoring = False
        
        # Basic calculations
        total_time = end_time - self.start_time if self.start_time else 0
        total_keystrokes = len(self.events)
        actual_chars = len(final_text)
        
        # Filter type events for interval calculation
        type_events = [e for e in self.events if e.event_type in ('type', 'composition')]
        
        # Calculate intervals
        intervals = []
        for i in range(1, len(type_events)):
            interval = type_events[i].timestamp - type_events[i-1].timestamp
            intervals.append(interval)
        
        # Average interval
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        
        # Characters per minute
        cpm = (actual_chars / total_time * 60) if total_time > 0 else 0
        
        # Consistency (coefficient of variation)
        consistency = self._calculate_consistency(intervals)
        
        # Pause analysis
        short_pauses = sum(1 for i in intervals if 2 <= i < 5)
        medium_pauses = sum(1 for i in intervals if 5 <= i < 15)
        long_pauses = sum(1 for i in intervals if i >= 15)
        
        if long_pauses > 0:
            pause_pattern = "contemplative"
        elif medium_pauses > 0:
            pause_pattern = "thoughtful"
        elif short_pauses > 0:
            pause_pattern = "choppy"
        else:
            pause_pattern = "continuous"
        
        # Deletion analysis
        deletion_count = sum(1 for e in self.events if e.event_type in ('backspace', 'delete'))
        deletion_ratio = deletion_count / total_keystrokes if total_keystrokes > 0 else 0
        
        # Burst detection
        burst_count, burst_segments, max_burst_speed = self._detect_bursts(intervals)
        
        # Hesitation mapping
        hesitation_count = sum(1 for i in intervals if i >= 3)
        hesitation_locations = [idx for idx, i in enumerate(intervals) if i >= 3]
        
        # Fluency calculation
        stability_score = consistency
        deletion_score = max(0, 1 - deletion_ratio * 2)
        pause_score = max(0, 1 - (short_pauses + medium_pauses * 2 + long_pauses * 3) / 10)
        hesitation_score = max(0, 1 - hesitation_count / 5)
        
        fluency_score = (0.30 * stability_score + 0.30 * deletion_score + 
                        0.20 * pause_score + 0.20 * hesitation_score)
        
        if fluency_score >= 0.8:
            fluency_level = "very_fluent"
        elif fluency_score >= 0.6:
            fluency_level = "fluent"
        elif fluency_score >= 0.4:
            fluency_level = "normal"
        else:
            fluency_level = "hesitant"
        
        # Rhythm type classification
        rhythm_type = self._classify_rhythm(cpm, consistency, pause_pattern)
        
        # Text rhythm analysis
        sentences = [s.strip() for s in final_text.replace('!', '.').replace('?', '.').replace('。', '.').replace('！', '.').replace('？', '.').split('.') if s.strip()]
        sentence_count = len(sentences) if sentences else 1
        avg_sentence_length = len(final_text) / sentence_count
        punctuation_count = sum(1 for c in final_text if c in '.,!?;:，。！？；：～~')
        punctuation_rate = punctuation_count / len(final_text) if final_text else 0
        
        # Text rhythm category
        if avg_sentence_length < 20 and punctuation_rate < 0.05:
            text_rhythm_category = "concise"
        elif avg_sentence_length < 20:
            text_rhythm_category = "staccato"
        elif avg_sentence_length >= 50 and punctuation_rate < 0.05:
            text_rhythm_category = "flowing"
        elif avg_sentence_length >= 50:
            text_rhythm_category = "complex"
        else:
            text_rhythm_category = "balanced"
        
        # Keystroke ratio
        keystroke_ratio = total_keystrokes / actual_chars if actual_chars > 0 else 0
        
        return {
            # Baseline Metrics (7)
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(total_time, 2),
            "chars_per_minute": round(cpm, 1),
            "pause_pattern": {
                "short_pauses": short_pauses,
                "medium_pauses": medium_pauses,
                "long_pauses": long_pauses,
                "pattern": pause_pattern
            },
            "consistency": round(consistency, 3),
            "text_rhythm": {
                "sentence_count": sentence_count,
                "avg_sentence_length": round(avg_sentence_length, 1),
                "punctuation_rate": round(punctuation_rate, 3),
                "rhythm_category": text_rhythm_category
            },
            "rhythm_type": rhythm_type,
            
            # Basic Statistics (3)
            "total_keystrokes": total_keystrokes,
            "actual_chars": actual_chars,
            "avg_interval": round(avg_interval, 3),
            
            # Deletion Analysis (3)
            "deletion_count": deletion_count,
            "deletion_ratio": round(deletion_ratio, 3),
            
            # Modification Analysis (2)
            "modification_count": 0,
            
            # Burst Detection (3)
            "burst_count": burst_count,
            "burst_segments": len(burst_segments),
            "max_burst_speed": round(max_burst_speed, 1),
            
            # Hesitation Mapping (3)
            "hesitation_count": hesitation_count,
            "hesitation_locations": hesitation_locations[:5],  # First 5 only
            
            # Fluency Scoring (2)
            "fluency_score": round(fluency_score, 3),
            "fluency_level": fluency_level,
            
            # Additional
            "keystroke_ratio": round(keystroke_ratio, 2)
        }
    
    def _calculate_consistency(self, intervals):
        if len(intervals) < 2:
            return 0.0
        mean = sum(intervals) / len(intervals)
        if mean == 0:
            return 0.0
        variance = sum((x - mean) ** 2 for x in intervals) / len(intervals)
        std_dev = sqrt(variance)
        cv = std_dev / mean
        return max(0.0, min(1.0, 1 - cv / 2))
    
    def _detect_bursts(self, intervals):
        bursts = []
        current_burst = 0
        burst_time = 0
        burst_start = 0
        
        for i, interval in enumerate(intervals):
            if interval < 0.15:  # 150ms threshold
                if current_burst == 0:
                    burst_start = i
                current_burst += 1
                burst_time += interval
            else:
                if current_burst >= 5:
                    speed = current_burst / burst_time if burst_time > 0 else 0
                    bursts.append({"start": burst_start, "length": current_burst, "speed": speed})
                current_burst = 0
                burst_time = 0
        
        if current_burst >= 5:
            speed = current_burst / burst_time if burst_time > 0 else 0
            bursts.append({"start": burst_start, "length": current_burst, "speed": speed})
        
        max_speed = max((b["speed"] for b in bursts), default=0)
        return len(bursts), bursts, max_speed
    
    def _classify_rhythm(self, cpm, consistency, pause_pattern):
        if cpm > 120:
            if consistency > 0.7:
                return "steady_fast" if pause_pattern == "continuous" else "burst_fast"
            return "erratic_fast"
        elif cpm < 60:
            if consistency > 0.7:
                return "steady_slow"
            return "hesitant" if pause_pattern in ("thoughtful", "contemplative") else "labored"
        else:
            if consistency > 0.7:
                return "fluid"
            return "measured" if pause_pattern == "thoughtful" else "uneven"


class RhythmTestGUI:
    """
    Standalone GUI Test Tool for CRPL
    💜 Test keystroke rhythm detection without CelestelinAgent
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎹 CRPL Rhythm Detector Test - by Yingying & Anran")
        self.root.geometry("750x650")
        self.root.configure(bg='#1a1a2e')
        
        self.detector = RhythmDetector()
        self.is_monitoring = False
        self.keystroke_count = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GUI"""
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=15)
        
        title = tk.Label(
            title_frame,
            text="🎹 CRPL Rhythm Detector Test",
            font=("Arial", 18, "bold"),
            fg='#a855f7',
            bg='#1a1a2e'
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="24 Fields • 7 Categories • Chinese/English Support",
            font=("Arial", 10),
            fg='#888',
            bg='#1a1a2e'
        )
        subtitle.pack()
        
        # Input section
        input_frame = tk.Frame(self.root, bg='#1a1a2e')
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        input_label = tk.Label(
            input_frame,
            text="📝 Type Here (支持中英文):",
            font=("Arial", 11),
            fg='white',
            bg='#1a1a2e'
        )
        input_label.pack(anchor=tk.W)
        
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 13),
            width=60,
            bg='#2d2d44',
            fg='white',
            insertbackground='white'
        )
        self.input_field.pack(fill=tk.X, pady=5)
        
        # Bind events
        self.input_field.bind("<FocusIn>", self.on_focus_in)
        self.input_field.bind("<Key>", self.on_key_press)
        self.input_field.bind("<Return>", lambda e: self.on_send())
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#1a1a2e')
        status_frame.pack(pady=5, padx=20, fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="⚪ Ready - Click input box to start",
            font=("Arial", 10),
            fg='#888',
            bg='#1a1a2e'
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.keystroke_label = tk.Label(
            status_frame,
            text="⌨️ Keystrokes: 0",
            font=("Arial", 10),
            fg='#4ade80',
            bg='#1a1a2e'
        )
        self.keystroke_label.pack(side=tk.RIGHT)
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg='#1a1a2e')
        btn_frame.pack(pady=10)
        
        self.send_btn = tk.Button(
            btn_frame,
            text="📊 Analyze",
            font=("Arial", 11, "bold"),
            command=self.on_send,
            bg='#a855f7',
            fg='white',
            padx=20,
            pady=5
        )
        self.send_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            btn_frame,
            text="🔄 Reset",
            font=("Arial", 11),
            command=self.on_clear,
            bg='#4b5563',
            fg='white',
            padx=20,
            pady=5
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Results section
        result_label = tk.Label(
            self.root,
            text="📊 Analysis Results:",
            font=("Arial", 11, "bold"),
            fg='white',
            bg='#1a1a2e'
        )
        result_label.pack(pady=(10, 5), anchor=tk.W, padx=20)
        
        self.result_text = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 10),
            height=22,
            width=85,
            bg='#2d2d44',
            fg='#e0e0e0',
            insertbackground='white'
        )
        self.result_text.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        # Initial message
        self.log("💜 CRPL Rhythm Detector Test Tool")
        self.log("=" * 60)
        self.log("Click the input box and start typing...")
        self.log("Press Enter or click 'Analyze' to see results.")
        self.log("")
        self.log("💡 Supports both Chinese (Pinyin) and English input!")
        self.log("💡 keystroke_ratio for Chinese: typically 3.0-4.0")
        self.log("")
        
        # Footer
        footer = tk.Label(
            self.root,
            text="💜 CelestelinAgent Research © 2025 • Yingying Chen & Anran Lin",
            font=("Arial", 9),
            fg='#666',
            bg='#1a1a2e'
        )
        footer.pack(pady=10)
    
    def on_focus_in(self, event):
        """Start monitoring when input field gets focus"""
        if not self.is_monitoring:
            self.detector.start_monitoring()
            self.is_monitoring = True
            self.keystroke_count = 0
            
            self.status_label.config(text="🟢 Recording...", fg='#4ade80')
            self.keystroke_label.config(text="⌨️ Keystrokes: 0")
    
    def on_key_press(self, event):
        """Record each keystroke"""
        if not self.is_monitoring:
            return
        
        if event.keysym == "Return":
            return
        
        if event.keysym == "BackSpace":
            self.detector.record_keystroke("", "backspace")
        elif event.keysym == "Delete":
            self.detector.record_keystroke("", "delete")
        else:
            char = event.char if event.char else ""
            self.detector.record_keystroke(char, "type")
        
        self.keystroke_count += 1
        self.keystroke_label.config(text=f"⌨️ Keystrokes: {self.keystroke_count}")
    
    def on_send(self):
        """Analyze and display results"""
        if not self.is_monitoring:
            self.log("⚠️ Please click the input box first!")
            return
        
        text = self.input_field.get().strip()
        
        if not text:
            self.log("⚠️ Please type something!")
            return
        
        result = self.detector.finish_monitoring(text)
        self.is_monitoring = False
        self.status_label.config(text="⚪ Ready", fg='#888')
        
        self.display_result(text, result)
        self.input_field.delete(0, tk.END)
    
    def on_clear(self):
        """Reset everything"""
        self.is_monitoring = False
        self.keystroke_count = 0
        self.input_field.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.status_label.config(text="⚪ Ready", fg='#888')
        self.keystroke_label.config(text="⌨️ Keystrokes: 0")
        self.log("🔄 Reset complete. Click input box to start again.")
    
    def display_result(self, text, data):
        """Display analysis results"""
        self.result_text.delete(1.0, tk.END)
        
        self.log("=" * 60)
        self.log(f"💜 CRPL Rhythm Analysis Results")
        self.log(f"📝 Text: {text[:50]}{'...' if len(text) > 50 else ''}")
        self.log("=" * 60)
        
        # Key metrics
        self.log("\n🎯 KEY METRICS:")
        self.log(f"   rhythm_type      : {data.get('rhythm_type', 'N/A')}")
        self.log(f"   fluency_score    : {data.get('fluency_score', 0)}")
        self.log(f"   fluency_level    : {data.get('fluency_level', 'N/A')}")
        self.log(f"   keystroke_ratio  : {data.get('keystroke_ratio', 0)} {'(Chinese IME detected!)' if data.get('keystroke_ratio', 0) > 2 else ''}")
        
        # Baseline Metrics
        self.log("\n📊 BASELINE METRICS (7 fields):")
        self.log(f"   duration_seconds : {data.get('duration_seconds', 0)} s")
        self.log(f"   chars_per_minute : {data.get('chars_per_minute', 0)}")
        self.log(f"   consistency      : {data.get('consistency', 0)}")
        pause = data.get('pause_pattern', {})
        self.log(f"   pause_pattern    : {pause.get('pattern', 'N/A')}")
        self.log(f"     - short (2-5s) : {pause.get('short_pauses', 0)}")
        self.log(f"     - medium (5-15s): {pause.get('medium_pauses', 0)}")
        self.log(f"     - long (>15s)  : {pause.get('long_pauses', 0)}")
        text_rhythm = data.get('text_rhythm', {})
        self.log(f"   text_rhythm      : {text_rhythm.get('rhythm_category', 'N/A')}")
        
        # Basic Statistics
        self.log("\n📈 BASIC STATISTICS (3 fields):")
        self.log(f"   total_keystrokes : {data.get('total_keystrokes', 0)}")
        self.log(f"   actual_chars     : {data.get('actual_chars', 0)}")
        self.log(f"   avg_interval     : {data.get('avg_interval', 0)} s")
        
        # Deletion & Modification
        self.log("\n✂️ DELETION & MODIFICATION (5 fields):")
        self.log(f"   deletion_count   : {data.get('deletion_count', 0)}")
        self.log(f"   deletion_ratio   : {data.get('deletion_ratio', 0)}")
        self.log(f"   modification_cnt : {data.get('modification_count', 0)}")
        
        # Burst Detection
        self.log("\n💥 BURST DETECTION (3 fields):")
        self.log(f"   burst_count      : {data.get('burst_count', 0)}")
        self.log(f"   burst_segments   : {data.get('burst_segments', 0)}")
        self.log(f"   max_burst_speed  : {data.get('max_burst_speed', 0)} chars/s")
        
        # Hesitation Mapping
        self.log("\n🤔 HESITATION MAPPING (3 fields):")
        self.log(f"   hesitation_count : {data.get('hesitation_count', 0)}")
        self.log(f"   locations (first5): {data.get('hesitation_locations', [])}")
        
        # Fluency Scoring
        self.log("\n🌊 FLUENCY SCORING (2 fields):")
        self.log(f"   fluency_score    : {data.get('fluency_score', 0)}")
        self.log(f"   fluency_level    : {data.get('fluency_level', 'N/A')}")
        
        self.log("\n" + "=" * 60)
        self.log("💜 Click input box to test again!")
    
    def log(self, message):
        """Add log message"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
    
    def run(self):
        """Run the GUI"""
        print("\n💜 CRPL Rhythm Detector Test Tool Started!")
        print("💜 Close the window to exit.\n")
        self.root.mainloop()


if __name__ == "__main__":
    print("\n" + "🎹" * 20)
    print("   CRPL Rhythm Detector GUI Test")
    print("   💜 by Yingying Chen & Anran Lin")
    print("🎹" * 20 + "\n")
    
    app = RhythmTestGUI()
    app.run()
