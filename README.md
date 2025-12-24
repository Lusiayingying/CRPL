# CRPL: Celestelin Rhythm Perception Layer

[![arXiv](https://img.shields.io/badge/arXiv-2412.xxxxx-b31b1b.svg)](https://arxiv.org/abs/2412.xxxxx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Affective Typing Patterns: A Fine-Grained Keystroke-Rhythm Perception Layer for Multi-Agent Cognition Systems**

CRPL is a novel framework that models keystroke rhythm as a perceptual signal for inferring users' cognitive and emotional states. Unlike traditional keystroke dynamics research focused on security authentication, CRPL positions typing rhythm as a foundation for AI agent perception and empathetic response generation.

![CRPL Architecture](docs/CRPL_Architecture.svg)

## ✨ Key Features

- **24 Fine-Grained Behavioral Features** organized into 7 functional categories
- **Real-Time Rhythm Detection** with millisecond-precision timestamps
- **Cross-Language Support** including Chinese IME (Pinyin) input
- **Agent Integration Patterns** for LLM-based systems
- **Interactive Demo Tools** (GUI + Web)

## 📊 Feature Categories

| Category | Fields | Description |
|----------|--------|-------------|
| 🎯 Baseline Metrics | 7 | Core rhythm signature (CPM, consistency, rhythm_type) |
| 📈 Basic Statistics | 3 | Aggregate metrics (keystrokes, chars, intervals) |
| 🔄 Deletion Analysis | 3 | Self-correction patterns |
| ✏️ Modification Analysis | 2 | Intent revision behavior |
| 💥 Burst Detection | 3 | Rapid typing segments |
| 🤔 Hesitation Mapping | 3 | Pause location distribution |
| 🌊 Fluency Scoring | 2 | Overall fluency assessment |

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/CelestelinAgent/CRPL.git
cd CRPL
pip install -r requirements.txt
```

### Basic Usage

```python
from crpl import RhythmDetector

# Initialize detector
detector = RhythmDetector()

# Start monitoring
detector.start_monitoring()

# Record keystrokes (integrate with your input handler)
detector.record_keystroke('H', 'type')
detector.record_keystroke('i', 'type')
# ... more keystrokes ...

# Get analysis results
results = detector.finish_monitoring("Hi there!")
print(results)
```

### Output Example

```json
{
  "timestamp": "2024-12-24T02:30:00Z",
  "duration_seconds": 15.5,
  "chars_per_minute": 85.2,
  "rhythm_type": "fluid",
  "consistency": 0.823,
  "fluency_score": 0.891,
  "fluency_level": "very_fluent",
  "burst_count": 3,
  "hesitation_count": 1,
  "deletion_ratio": 0.05,
  "pause_pattern": {
    "short_pauses": 2,
    "medium_pauses": 0,
    "long_pauses": 0,
    "pattern": "choppy"
  }
}
```

## 🖥️ Demo Tools

### GUI Demo (Python/Tkinter)

Best for accurate Chinese IME capture:

```bash
python demo/test_rhythm_gui.py
```

### Web Demo (React)

For quick testing and visualization:

```bash
cd demo/web
npm install
npm start
```

## 🎭 Rhythm Types

CRPL classifies typing rhythm into 10 distinct types:

| Type | Speed | Consistency | Interpretation |
|------|-------|-------------|----------------|
| `steady_fast` | >120 CPM | High | Confident, skilled |
| `burst_fast` | >120 CPM | High | Inspired, energized |
| `fluid` | 60-120 CPM | High | Flow state |
| `measured` | 60-120 CPM | Low | Analytical thinking |
| `hesitant` | <60 CPM | Low | Uncertain, exploring |
| `labored` | <60 CPM | Low | Struggling, fatigued |

## 🔌 Agent Integration

### Pattern 1: Pre-Response Analysis

```python
async def generate_response(user_input, rhythm_data):
    if rhythm_data["rhythm_type"] == "hesitant":
        # User seems uncertain - be supportive
        system_prompt += "Be encouraging and offer help."
    elif rhythm_data["burst_count"] > 10:
        # User is energized - match their energy
        system_prompt += "Be enthusiastic and engaged."
    
    return await llm.generate(system_prompt, user_input)
```

### Pattern 2: Real-Time Adaptation

```python
def on_hesitation_detected(duration, location):
    if duration > 5:  # 5+ second pause
        # Prepare contextual help
        show_typing_suggestions()
```

## 🌏 Chinese IME Support

CRPL handles Chinese Pinyin input with specialized adaptation:

| Metric | English | Chinese (Pinyin) |
|--------|---------|------------------|
| keystroke_ratio | ≈1.0 | 3.0-4.0 |
| Capture method | Direct | Composition Events |

The system correctly interprets higher keystroke ratios as normal for Chinese input rather than indicating difficulty.

## 📝 Citation

If you use CRPL in your research, please cite:

```bibtex
@article{chen2024crpl,
  title={Affective Typing Patterns: A Fine-Grained Keystroke-Rhythm Perception Layer for Multi-Agent Cognition Systems},
  author={Chen, Yingying and Lin, Anran},
  journal={arXiv preprint arXiv:2412.xxxxx},
  year={2024}
}
```

## 📁 Repository Structure

```
CRPL/
├── README.md
├── requirements.txt
├── LICENSE
├── crpl/
│   ├── __init__.py
│   ├── detector.py          # Core RhythmDetector class
│   ├── analyzer.py          # Feature analysis algorithms
│   └── types.py             # Data types and enums
├── demo/
│   ├── test_rhythm_gui.py   # Tkinter GUI demo
│   └── web/
│       └── RhythmDetectorPro.jsx  # React web demo
├── docs/
│   ├── CRPL_Architecture.svg
│   └── paper.pdf
└── examples/
    └── agent_integration.py  # Example agent integration
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Yingying Chen** - Independent Researcher, Calgary, Canada
- **Anran Lin** - CelestelinAgent Research Group

## 🙏 Acknowledgments

This work is part of the [CelestelinAgent](https://github.com/CelestelinAgent) project, exploring new dimensions of human-AI interaction.

---

<p align="center">
  <i>"The typing patterns humans produce are not noise to be filtered—they are signals worth perceiving."</i>
</p>

<p align="center">
  💜 CelestelinAgent Research © 2025
</p>
