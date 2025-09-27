````markdown
# 🛡️ Cloudless SOC: Brute Force Detection

A Python/Streamlit web app that ingests authentication logs, finds bursty failed-logon activity with a sliding window, and shows results in a clean dashboard.

![Demo](demo.gif)

---

## ✨ Features
- **Web UI**: Upload a CSV of auth events and tune detection from the sidebar.
- **Sliding window detection**: Pick window size (minutes) and failure threshold to flag brute-force bursts.
- **KPI cards**: Total events, failed logons, and unique source IPs at a glance.
- **Professional chart**: Area chart for the top `src_ip → user` offender with a visible threshold line.
- **Alerts table**: Sortable table of hits with timestamp, source IP, user, failures, and a rule label.
- **Export**: One-click download of alerts as CSV.
- **Cross-platform**: Works on Windows, macOS, and Linux.

---

## 🚀 Quick Start (Local Demo)

```bash
git clone https://github.com/AdonisYounes/cloudless-soc-vscode.git
cd cloudless-soc-vscode

python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
````

Open the local URL (usually [http://localhost:8501](http://localhost:8501)), upload a CSV, and adjust the sliders.

---

## 📄 Input Format

Headers:

```
timestamp,src_ip,user,event_id,status
```

Example:

```csv
2025-09-26T12:30:01,198.51.100.66,Administrator,4625,failed
```

---

## 🧠 How It Works

1. Filter failed logons.
2. Group by `(src_ip, user)` and apply a rolling window.
3. Count failures per window; alert when count ≥ threshold.
4. Chart the top offender and list alerts in the table.

---

## 🛠️ Tips

* No alerts? Lower threshold or increase window.
* Ensure headers match exactly and timestamps are parseable.

```
```
