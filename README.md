# Deadlock & Banker’s Algorithm Dashboard

A simple Streamlit app for an Operating Systems activity.

## Features
- Animated interactive Deadlock Simulation in Replay Mode with step-by-step playback & recovery
- Need matrix calculation (`Need = Max - Allocation`)
- Banker’s Algorithm safety check and safe sequence
- Resource request validation and safety check
- Separate deadlock detection example with recovery action
- Deadlock prevention policies
- Boundary and invalid-input test cases
- Activity test report with CSV download

## Run on Windows
1. Install Python 3.10 or newer.
2. Extract this ZIP folder.
3. Open Command Prompt in the extracted folder.
4. Run:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Your browser should open the dashboard. If not, visit the local URL printed in the terminal (usually `http://localhost:8501`).

## Recommended demo order
1. Overview
2. Banker’s Algorithm — show the Need matrix and safe sequence
3. Resource Request — try P4 request `(3,3,0)` for unsafe-state rejection
4. Scenario B — set Available to `(1,1,1)` and request `(1,2,2)` from P1
5. Deadlock Detection — show the circular wait and recovery
6. Deadlock Prevention
7. Boundary Tests and Activity Test Report

## Notes
- The default example is a standard five-process, three-resource Banker’s Algorithm example.
- The app keeps matrices in the Streamlit session, not in a database.
- The app intentionally distinguishes unsafe states from confirmed deadlocks.
- Check and record actual test results before submitting your assignment.
