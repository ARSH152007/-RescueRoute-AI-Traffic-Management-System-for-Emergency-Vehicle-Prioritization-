import streamlit as st
import subprocess
import time
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# ⚙️ CONFIG
# =========================
st.set_page_config(page_title="RescueRoute AI", layout="wide")

# =========================
# 🎨 MODERN DASHBOARD UI
# =========================
st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
    color: #0f172a;
}

h1 {
    font-size: 38px !important;
    font-weight: 900;
    color: #0f172a;
}

.card {
    background: rgba(255,255,255,0.95);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-3px);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#2563eb,#22c55e);
    color: white;
    font-weight: 700;
    border-radius: 12px;
}

/* Metric */
.metric {
    font-size: 28px;
    font-weight: 900;
}

.small {
    color: #64748b;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚦 RescueRoute AI Traffic Intelligence System")
st.caption("AI Traffic Optimization • Emergency Priority Routing • SUMO Simulation Dashboard")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Control Panel")

steps = st.sidebar.slider("Simulation Steps", 500, 3000, 1500)
mode = st.sidebar.selectbox("Mode", ["AI", "NORMAL"])

start = st.sidebar.button("▶️ Run Simulation")

st.sidebar.markdown("""
###  System Modes
- 🟢 AI → Smart RL + Prediction  
- ⚪ NORMAL → Fixed Traffic System  
""")

# =========================
# 🚦 TRAFFIC STATUS FUNCTION (NEW)
# =========================
def get_traffic_status(avg_wait):
    if avg_wait < 1:
        return "🟢 LOW TRAFFIC", "Smooth traffic flow"
    elif avg_wait < 3:
        return "🟡 MEDIUM TRAFFIC", "Moderate congestion detected"
    else:
        return "🔴 HIGH TRAFFIC", "Heavy congestion present"

# =========================
# RUN
# =========================
if start:

    st.info("Simulation Running... Please wait ⏳")

    progress = st.progress(0)

    process = subprocess.Popen(["python", "main.py", str(steps), mode])

    for i in range(100):
        time.sleep(0.02)
        progress.progress(i + 1)

    process.wait()

    file_path = "results.json"

    while not os.path.exists(file_path):
        time.sleep(1)

    with open(file_path, "r") as f:
        data = json.load(f)

    st.success("Simulation Completed ✅")

    # =========================
    # DASHBOARD METRICS
    # =========================
    st.subheader("📊 Live System Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"""
    <div class="card">
        <div class="small">⏱ Average Waiting Time</div>
        <div class="metric">{round(data["average_waiting_time"],3)}</div>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class="card">
        <div class="small">🚑 Ambulances Detected</div>
        <div class="metric">{data.get("ambulances_handled",0)}</div>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class="card">
        <div class="small">⚙️ Active Mode</div>
        <div class="metric">{mode}</div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # 🚦 TRAFFIC STATUS (NEW ADDITION)
    # =========================
    st.subheader("🚦 Real-Time Traffic Status")

    status, desc = get_traffic_status(data["average_waiting_time"])

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h2>{status}</h2>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # TABS
    # =========================
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 AI Learning",
        "📈 Traffic Flow",
        "🚑 Emergency System",
        "📋 Research Insights"
    ])

    # =========================
    # Q TABLE
    # =========================
    with tab1:
        st.subheader("Reinforcement Learning Q-Table")

        df = pd.DataFrame(
            data["q_table"],
            columns=["Green 10s", "Green 20s", "Green 30s"]
        )

        df.index = [f"State {i}" for i in range(len(df))]
        df["Best Action"] = df.idxmax(axis=1)

        st.dataframe(df, use_container_width=True)

    # =========================
    # GRAPH
    # =========================
    with tab2:
        st.subheader("Traffic Congestion Trend")

        w = data.get("waiting_times", [])

        if w:
            fig, ax = plt.subplots()
            ax.plot(w, linewidth=2, color="#2563eb")
            ax.set_xlabel("Step")
            ax.set_ylabel("Waiting Time")
            st.pyplot(fig)
        else:
            st.warning("No data available")

    # =========================
    # EMERGENCY
    # =========================
    with tab3:
        st.subheader("🚑 Emergency Intelligence Layer")

        total = data.get("ambulances_handled", 0)

        if mode == "AI":
            if total > 0:
                st.success("🚀 Emergency System ACTIVE (Green Corridor ON)")
                st.write("""
                - Real-time ambulance detection  
                - Dynamic route clearing  
                - Priority-based signal override  
                """)
            else:
                st.info("No ambulance detected")
        else:
            st.warning("NORMAL MODE → Emergency system inactive")

    # =========================
    # INSIGHTS
    # =========================
    with tab4:
        st.subheader("Research Analysis Report")

        if mode == "NORMAL":
            st.error("BASELINE SYSTEM (NO AI)")
            st.write("""
            - Fixed signal timing  
            - No learning  
            - Used for comparison  
            """)
        else:
            st.success("AI-ENABLED SYSTEM")
            st.write("""
            - RL based optimization  
            - Traffic prediction  
            - Emergency prioritization  
            """)

        avg = data["average_waiting_time"]

        st.subheader("Final Observation")

        if avg < 1:
            st.success("Excellent traffic optimization 🚀")
        elif avg < 3:
            st.info("Moderate performance")
        else:
            st.warning("High congestion detected")