# app.py — Cloudless SOC (Brute-Force Detector) with branding + sleek Plotly chart
# Run: python -m streamlit run app.py

import io
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# --------------------------- Page / Theme ------------------------------------
st.set_page_config(
    page_title="Cloudless SOC — Brute Force Detector",
    page_icon="🔐",
    layout="wide",
)

# --- Branding (header byline + sticky footer copyright) ---
st.markdown(
    """
    <style>
      .small-byline { font-size: 0.9rem; color: #9aa0a6; margin-top: -12px; }
      /* Hide default footer then add a custom one */
      .reportview-container .main footer {visibility: hidden;}
      footer:after {
        content: "© 2025 Adonis Younes — Cloudless SOC";
        visibility: visible;
        display: block;
        position: fixed;
        bottom: 10px;
        right: 16px;
        font-size: 0.85rem;
        color: #9aa0a6;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔐 Cloudless SOC — Brute Force Detection")
st.markdown('<div class="small-byline">by <b>Adonis Younes</b></div>', unsafe_allow_html=True)
st.caption("Parse auth logs, spot brute-force bursts, and export alerts. No VMs required.")

# --------------------------- Sidebar Controls --------------------------------
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("Tune detection parameters and upload a CSV of auth events.")

window_minutes = st.sidebar.slider("Rolling window (minutes)", 1, 30, 5, 1)
threshold = st.sidebar.slider("Failure threshold", 2, 50, 8, 1)

uploaded = st.sidebar.file_uploader(
    "Upload CSV (timestamp,src_ip,user,event_id,status)", type=["csv"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Sample schema**")
st.sidebar.code(
    "timestamp,src_ip,user,event_id,status\n"
    "2025-09-26T12:30:01,198.51.100.66,Administrator,4625,FAIL"
)

# --------------------------- Data Loading ------------------------------------
@st.cache_data
def load_default_data():
    return pd.read_csv("data/sample_windows_security.csv", parse_dates=["timestamp"])

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded, parse_dates=["timestamp"])
        st.success("Custom data loaded.")
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")
        df = load_default_data()
else:
    df = load_default_data()

# Basic typing / safety
for col in ["user", "src_ip", "status"]:
    if col in df.columns:
        df[col] = df[col].astype(str)

# --------------------------- KPIs --------------------------------------------
total_rows = len(df)
total_fails = int(((df.get("status") == "FAIL") & (df.get("event_id") == 4625)).sum())
unique_ips = df.get("src_ip", pd.Series(dtype=str)).nunique()

k1, k2, k3 = st.columns(3)
k1.metric("Total Events", f"{total_rows:,}")
k2.metric("Failed Logons (4625)", f"{total_fails:,}")
k3.metric("Unique Source IPs", f"{unique_ips:,}")

# --------------------------- Detection Logic ---------------------------------
fails = df[(df.get("status") == "FAIL") & (df.get("event_id") == 4625)].copy()

if not fails.empty:
    fails = fails.sort_values("timestamp").set_index("timestamp")
    window_str = f"{window_minutes}min"
    group_cols = ["src_ip", "user"]
    # Count failures per src_ip→user per time window
    counts = (
        fails.groupby(group_cols)
        .resample(window_str)
        .size()
        .reset_index(name="failures")
    )
    # Suspicious windows
    sus = counts[counts["failures"] >= threshold].copy()
else:
    counts = pd.DataFrame(columns=["src_ip", "user", "timestamp", "failures"])
    sus = counts.copy()

# --------------------------- Chart (Plotly) ----------------------------------
st.subheader("📈 Failures Over Time (Top Offender)")

if not sus.empty:
    offenders = sus.groupby("src_ip")["failures"].sum().sort_values(ascending=False)
    top_ip = offenders.index[0]

    top_df = counts[counts["src_ip"] == top_ip]
    top_user = (
        top_df.groupby("user")["failures"].sum().sort_values(ascending=False).index[0]
    )
    plot_df = top_df[top_df["user"] == top_user].sort_values("timestamp")

    fig = go.Figure()

    # Smooth line + subtle area fill (finance-app feel)
    fig.add_trace(
        go.Scatter(
            x=plot_df["timestamp"],
            y=plot_df["failures"],
            mode="lines",
            line=dict(width=3, shape="spline"),
            fill="tozeroy",
            hovertemplate="%{x|%Y-%m-%d %H:%M}<br><b>Failures</b>: %{y}<extra></extra>",
            name=f"{top_ip} → {top_user}",
        )
    )

    # Dotted threshold line
    fig.add_hline(
        y=threshold,
        line_dash="dot",
        opacity=0.6,
        annotation_text=f"Threshold = {threshold}",
        annotation_position="top left",
    )

    # Minimal, modern layout
    fig.update_layout(
        title=f"Failed Logons — {top_ip} → {top_user}",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=False, showspikes=True, spikemode="across", spikesnap="cursor"),
        yaxis=dict(title="Failures per window", showgrid=False, zeroline=False),
        hovermode="x unified",
        showlegend=False,
        height=420,
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(
        "No suspicious windows found at current threshold. "
        "Try lowering the threshold or widening the window."
    )

# --------------------------- Alerts Table ------------------------------------
st.subheader("🚨 Alerts")

if not sus.empty:
    alerts = sus.copy()
    alerts["rule"] = f"BruteForce_{window_minutes}min_{threshold}"
    alerts_sorted = alerts.sort_values(["failures", "timestamp"], ascending=[False, True])

    st.dataframe(alerts_sorted, use_container_width=True)

    csv_buf = io.StringIO()
    alerts_sorted.to_csv(csv_buf, index=False)
    st.download_button(
        "Download Alerts CSV",
        csv_buf.getvalue(),
        file_name="alerts.csv",
        mime="text/csv",
    )
else:
    st.write("No alerts at the moment.")

# --------------------------- Help Expander -----------------------------------
with st.expander("ℹ️ How to read these results"):
    st.markdown(
        """
**Window** groups failures in rolling time buckets (e.g., 5 minutes).  
**Threshold** triggers an alert if failures in a bucket for the same `src_ip` → `user` pair meet or exceed the number.

**Tips**
- Smaller window = catches fast attacks; larger window = catches slow drips.
- Lower threshold = more sensitive; higher threshold = stricter.
- Next steps after an alert: GeoIP lookup, temporary block, account lockout review, MFA audit, password reset.
"""
    )

