# Cloudless SOC — VS Code Starter

A lightweight, **VS Code + Jupyter** project that detects simple brute-force login activity from logs — no virtual machines required.

## What this is
- A **Jupyter Notebook** you can run directly in VS Code
- A small **sample dataset** that mimics Windows Security logins
- A simple **detection pipeline**: parse → aggregate → alert → visualize
- A place to add **Sigma rules** and your own datasets

## Quick Start (VS Code)
1. Install **Python 3.10+**.
2. Install **VS Code** and these extensions:
   - *Python* (ms-python.python)
   - *Jupyter* (ms-toolsai.jupyter)
3. In a terminal at the project root, create a virtual env and install deps:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Open `notebooks/brute_force_detection.ipynb` in VS Code and **Run All**.

## What to put on your resume
> Built a **Cloudless SOC** notebook in VS Code to parse Windows-style auth logs, detect brute-force patterns, enrich with threat intel, and generate a brief incident report with charts.

## Next Steps / Ideas
- Replace sample data with real open-source logs (Kaggle/BTLO/Security Onion PCAP-derived)
- Add **Sigma** detection rules under `sigma-rules/` and map to **MITRE ATT&CK**
- Add **GitHub Actions** to lint rules and run notebook tests (papermill)
- Write an incident report under `reports/` with screenshots of your charts

---

**Folders**

```
cloudless-soc-vscode/
├─ README.md
├─ requirements.txt
├─ data/
│  └─ sample_windows_security.csv
├─ notebooks/
│  └─ brute_force_detection.ipynb
├─ sigma-rules/
│  └─ suspicious_powershell.yml
└─ scripts/
   └─ generate_synthetic_log.py
```

Have fun and break things (safely) 🔐
