# Mini Paint — CG Capstone Project

A 2D vector drawing application built with Python and OpenGL (GLUT).

## Requirements

```bash
pip install PyOpenGL PyOpenGL_accelerate
# Linux also needs:
sudo apt install freeglut3
```

## Run

```bash
python main.py
```

## Project Structure

```
MiniPaint/
├── main.py                        # Entry point
├── core/
│   ├── constants.py               # World range, palette, cfg dict
│   ├── viewport.py                # Screen ↔ world coordinate mapping
│   └── renderer.py                # Grid, shape drawing, rubber-band preview
├── shapes/
│   ├── shape.py                   # Base Shape class + Tool constants
│   ├── line.py                    # Line factory
│   ├── polyline.py                # Polyline factory
│   ├── polygon.py                 # Regular polygon factory + vertex math
│   └── shape_manager.py           # Canvas list: commit, undo, delete, clear
├── transform/
│   ├── matrix.py                  # Pure-Python T·R·S point transform
│   ├── transform.py               # OpenGL matrix push (apply_transform)
│   └── transform_manager.py       # Keyboard-driven transform commands
├── input/
│   ├── mouse_handler.py           # GLUT mouse callbacks
│   └── keyboard_handler.py        # GLUT keyboard + special-key callbacks
├── selection/
│   └── selection_manager.py       # Hit-testing + selection state
└── ui/
    └── ui_manager.py              # Sidebar panel + status bar
```

## Controls

| Key / Action | Effect |
|---|---|
| L | Line tool |
| P | Polyline tool |
| G | Polygon tool |
| S | Select tool |
| F | Toggle fill |
| [ / ] | Decrease / increase line width |
| + / - | More / fewer polygon sides |
| 0–9 | Select colour |
| Enter | Finish polyline |
| Z | Undo |
| Del | Delete selected shape |
| C | Clear canvas |
| Esc | Cancel current drawing |
| **Select mode** | |
| Arrow keys | Translate shape |
| R / E | Rotate CCW / CW |
| = / - | Uniform scale up / down |
| X / x | Scale X up / down |
| Y / y | Scale Y up / down |

## Core Concepts Demonstrated

- **Window-to-Viewport Mapping** — `core/viewport.py`
- **2D Affine Transformation Sequences** (T·R·S) — `transform/matrix.py`, `transform/transform.py`
- **Mouse & Keyboard Callbacks** — `input/`
- **Vector shape storage** (no pixel manipulation) — `shapes/

## Members

| Full Name        | ID          |
| ---------------- | ----------- |
| Abebaye Agumasie | UGR/9919/16 |
| Hemen Solomon    | UGR/1728/16 |
| Israel Shimeles  | UGR/7570/16 |
| Nanat Abeshu     | UGR/6300/16 |
| Tsion Tibebe     | UGR/5794/16 |
| Kaleab Lemma     | UGR/2941/16 |
