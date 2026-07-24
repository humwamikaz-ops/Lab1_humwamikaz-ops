# Lab1_humwamikaz-ops
# Student Performance & Grade Evaluator

A Python and Bash utility suite designed to process student academic performance records, evaluate pass/fail criteria, calculate overall GPA, and manage data archiving.

---

## Features

- **Grade Evaluation (`grade-evaluator.py`)**:
  - Parses student assessment records from a target CSV file (`filetarget`).
  - Validates score bounds (0–100%) and strict weight distribution rules (100% total: 40% Summative, 60% Formative).
  - Calculates final weighted percentages and overall GPA on a 5.0 scale.
  - Automatically flags resubmission candidates based on top-weighted unpassed formative tasks.

- **File Organization & Archiving (`organizer.sh`)**:
  - Automates file management by relocating CSV grade records to an `./archive` directory.
  - Generates ISO timestamps for archived files to prevent overwriting.
  - Logs all structural modifications and execution activity to `organizer.log`.

---

## Requirements

- Python 3.x
- Bash Environment (Linux, macOS, or Git Bash on Windows)

---

## How to Run

### 1. Execute Grade Assessment

To process grades, execute the Python script and enter the target CSV file name when prompted:

```bash
python3 grade-evaluator.py
