# DFA Auto Simulator

A web-based Flask application that automatically generates a Deterministic Finite Automaton (DFA) from any input string and simulates it visually — no manual setup of states, alphabets, or transitions required.

## Overview

Traditional DFA tools require users to manually define states, alphabet, transition rules, start state, and final states. This project removes that friction entirely — just type a string, and the system builds the complete DFA for you, then lets you test other strings against it to see if they're accepted or rejected.

## Features

- **Automatic DFA construction** — generates states, transitions, and accepting states from any input string
- **Step-by-step simulation trace** — logs every transition (`delta(q0, 'a') → q1`)
- **Interactive visual graph** — color-coded DFA diagram rendered with HTML5 Canvas
- **Test any string** — check whether a different string is `ACCEPTED` or `REJECTED` against the generated DFA
- **Dead/trap state handling** — invalid transitions are routed to a trap state instead of crashing
- **No external dependencies** — graph rendering uses pure JavaScript/Canvas, no Graphviz installation needed

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Templating | Jinja2 |
| Graph Rendering | HTML5 Canvas (vanilla JS) |

## How It Works

1. Enter a **target string** (letters and digits supported) — e.g. `ab1c`
2. The app builds a DFA where:
   - Each character maps to a new state (`q0 → q1 → q2 ...`)
   - The final character's state becomes the **accepting state**
   - Any unexpected symbol routes to a **dead state**
3. Optionally enter a **test string** to simulate against the generated DFA
4. View the result:
   - `ACCEPTED` ✅ or `REJECTED` ❌
   - Full transition trace
   - Visual DFA graph with the active path highlighted

## DFA Definition

Each generated DFA follows the formal 5-tuple definition:
Q  → Set of states (q0, q1, ..., qN, qDead)

Σ  → Alphabet (unique symbols in the input string)

δ  → Transition function

q0 → Start state

F  → Set of accepting states ({qN})

## Installation & Setup

```bash
# Clone or download the project
cd "TOA project"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install flask

# Run the application
python main.py
```
## Project Structure
TOA project/

├── main.py              # Flask backend, DFA logic, simulation

├── templates/

│   └── index.html       # Frontend UI + Canvas graph rendering

├── venv/                # Virtual environment

└── README.md
