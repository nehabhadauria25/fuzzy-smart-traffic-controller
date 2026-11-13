import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from simulation import generate_arrivals, fixed_controller, simulate_traffic
from fuzzy_logic import fuzzy_controller


st.set_page_config(page_title="Smart Traffic Controller", page_icon="🚦", layout="wide")
st.title("🚦 Fuzzy Logic-Based Smart Traffic Controller")
st.write("Compare fixed-time and fuzzy-logic signals using the same vehicle arrivals.")

with st.sidebar:
    st.header("Simulation settings")
    minutes = st.slider("Duration (minutes)", 2, 30, 10)
    ns_rate = st.slider("North-South arrivals/sec", 0.05, 1.00, 0.35, 0.05)
    ew_rate = st.slider("East-West arrivals/sec", 0.05, 1.00, 0.30, 0.05)
    fixed_green = st.slider("Fixed green time (seconds)", 10, 60, 30, 5)
    seed = st.number_input("Random seed", 0, 99999, 42)

if st.button("Run simulation", type="primary"):
    seconds = minutes * 60
    arrivals = generate_arrivals(seconds, ns_rate, ew_rate, int(seed))
    with st.spinner("Running simulations..."):
        fixed = simulate_traffic(fixed_controller, arrivals, seconds, fixed_green)
        fuzzy = simulate_traffic(fuzzy_controller, arrivals, seconds, fixed_green)
    st.session_state["results"] = {"Fixed-Time": fixed, "Fuzzy Logic": fuzzy}

if "results" not in st.session_state:
    st.info("Set the options and click Run simulation.")
else:
    results = st.session_state["results"]
    fixed_metrics = results["Fixed-Time"]["metrics"]
    fuzzy_metrics = results["Fuzzy Logic"]["metrics"]

    st.subheader("Performance comparison")
    comparison = pd.DataFrame(
        [fixed_metrics, fuzzy_metrics],
        index=["Fixed-Time Controller", "Fuzzy Logic Controller"]
    ).T
    st.dataframe(comparison, use_container_width=True)

    improvement = (fixed_metrics["Average waiting time (sec)"]
                   - fuzzy_metrics["Average waiting time (sec)"])
    if improvement > 0:
        st.success(f"Fuzzy logic reduced average waiting by {improvement:.2f} seconds in this run.")
    elif improvement < 0:
        st.info(f"Fixed-time had lower average waiting by {abs(improvement):.2f} seconds in this run.")
    else:
        st.info("Both controllers had the same average waiting time in this run.")

    st.subheader("Queue length over time")
    fig, ax = plt.subplots(figsize=(11, 4))
    for label, result in results.items():
        h = result["history"]
        ax.plot(h["time"] / 60,
                h["total_queue"].rolling(15, min_periods=1).mean(),
                label=label)
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Queue length (15-second rolling average)")
    ax.set_title("Traffic queue comparison")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Green-light decisions")
    phase_tables = []
    for label, result in results.items():
        frame = result["phases"].copy()
        frame["controller"] = label
        phase_tables.append(frame)
    st.dataframe(pd.concat(phase_tables, ignore_index=True), use_container_width=True)

    st.download_button(
        "Download comparison CSV", comparison.to_csv().encode("utf-8"),
        "traffic_controller_comparison.csv", "text/csv"
    )

st.caption("Educational simulation only; not suitable for controlling real traffic signals.")
