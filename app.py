import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from simulation import (
    generate_arrivals,
    fixed_controller,
    simulate_traffic
)

from fuzzy_logic import fuzzy_controller

# Person 2: Performance Metrics
from traffic_metrics import (
    calculate_metrics,
    compare_controllers,
    get_congestion_level
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Traffic Controller",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Fuzzy Logic-Based Smart Traffic Controller")

st.write(
    "An intelligent traffic management system that compares "
    "fixed-time and fuzzy-logic-based adaptive traffic signals."
)


# --------------------------------------------------
# SIDEBAR: SIMULATION SETTINGS
# --------------------------------------------------

with st.sidebar:

    st.header("Simulation Settings")

    minutes = st.slider(
        "Duration (minutes)",
        2, 30, 10
    )

    ns_rate = st.slider(
        "North-South arrivals/sec",
        0.05, 1.00, 0.35, 0.05
    )

    ew_rate = st.slider(
        "East-West arrivals/sec",
        0.05, 1.00, 0.30, 0.05
    )

    fixed_green = st.slider(
        "Fixed green time (seconds)",
        10, 60, 30, 5
    )

    seed = st.number_input(
        "Random seed",
        0, 99999, 42
    )


# --------------------------------------------------
# RUN SIMULATION
# --------------------------------------------------

if st.button("Run Simulation", type="primary"):

    seconds = minutes * 60

    arrivals = generate_arrivals(
        seconds,
        ns_rate,
        ew_rate,
        int(seed)
    )

    with st.spinner("Running traffic simulations..."):

        fixed = simulate_traffic(
            fixed_controller,
            arrivals,
            seconds,
            fixed_green
        )

        fuzzy = simulate_traffic(
            fuzzy_controller,
            arrivals,
            seconds,
            fixed_green
        )

    st.session_state["results"] = {
        "Fixed-Time": fixed,
        "Fuzzy Logic": fuzzy
    }

    st.success("Simulation completed successfully!")


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "results" not in st.session_state:

    st.info("Configure the simulation settings and click Run Simulation.")

else:

    results = st.session_state["results"]

    fixed_result = results["Fixed-Time"]
    fuzzy_result = results["Fuzzy Logic"]

    fixed_metrics = fixed_result["metrics"]
    fuzzy_metrics = fuzzy_result["metrics"]


    # --------------------------------------------------
    # PERSON 2: CALCULATE PERFORMANCE METRICS
    # --------------------------------------------------

    fixed_summary = calculate_metrics(
        fixed_result["wait_times"],
        fixed_result["history"]["total_queue"].tolist(),
        [fixed_metrics["Vehicles crossed"]]
    )

    fuzzy_summary = calculate_metrics(
        fuzzy_result["wait_times"],
        fuzzy_result["history"]["total_queue"].tolist(),
        [fuzzy_metrics["Vehicles crossed"]]
    )


    # --------------------------------------------------
    # PERSON 2: COMPARE BOTH CONTROLLERS
    # --------------------------------------------------

    controller_comparison = compare_controllers(
        fixed_summary,
        fuzzy_summary
    )


    # --------------------------------------------------
    # PERSON 2: CONGESTION CLASSIFICATION
    # --------------------------------------------------

    fixed_congestion = get_congestion_level(
        fixed_summary["average_queue_length"]
    )

    fuzzy_congestion = get_congestion_level(
        fuzzy_summary["average_queue_length"]
    )


    # --------------------------------------------------
    # SECTION 1: PERFORMANCE OVERVIEW
    # --------------------------------------------------

    st.divider()

    st.header("📊 Performance Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Fixed-Time Controller")

        st.metric(
            "Average Waiting Time",
            f"{fixed_summary['average_waiting_time']} sec"
        )

        st.metric(
            "Average Queue Length",
            fixed_summary["average_queue_length"]
        )

        st.metric(
            "Vehicles Passed",
            fixed_summary["total_vehicles_passed"]
        )

        st.info(f"Congestion Level: {fixed_congestion}")


    with col2:

        st.subheader("Fuzzy Logic Controller")

        st.metric(
            "Average Waiting Time",
            f"{fuzzy_summary['average_waiting_time']} sec",
            delta=round(
                fixed_summary["average_waiting_time"]
                - fuzzy_summary["average_waiting_time"],
                2
            ),
            delta_description="Reduction compared with fixed-time"
        )

        st.metric(
            "Average Queue Length",
            fuzzy_summary["average_queue_length"]
        )

        st.metric(
            "Vehicles Passed",
            fuzzy_summary["total_vehicles_passed"]
        )

        st.success(f"Congestion Level: {fuzzy_congestion}")


    # --------------------------------------------------
    # SECTION 2: PERCENTAGE IMPROVEMENT
    # --------------------------------------------------

    st.divider()

    st.header("📈 Percentage Improvement")

    for metric, values in controller_comparison.items():

        st.write(
            f"**{metric.replace('_', ' ').title()}**"
        )

        improvement = values["improvement_percentage"]

        st.write(f"Improvement: {improvement}%")

        if improvement > 0:

            st.progress(
                min(abs(improvement) / 100, 1.0)
            )

        else:

            st.info("No positive improvement over fixed-time control.")


    # --------------------------------------------------
    # SECTION 3: DETAILED COMPARISON TABLE
    # --------------------------------------------------

    st.divider()

    st.header("📋 Detailed Simulation Results")

    comparison = pd.DataFrame(
        [fixed_metrics, fuzzy_metrics],
        index=[
            "Fixed-Time Controller",
            "Fuzzy Logic Controller"
        ]
    ).T

    st.dataframe(
        comparison,
        use_container_width=True
    )


    # --------------------------------------------------
    # SECTION 4: WAITING TIME COMPARISON
    # --------------------------------------------------

    st.divider()

    st.header("⏱️ Waiting Time Comparison")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        ["Fixed-Time", "Fuzzy Logic"],
        [
            fixed_summary["average_waiting_time"],
            fuzzy_summary["average_waiting_time"]
        ]
    )

    ax.set_ylabel("Average Waiting Time (seconds)")

    ax.set_title("Average Waiting Time Comparison")

    ax.grid(axis="y", alpha=0.3)

    st.pyplot(fig)

    plt.close(fig)


    # --------------------------------------------------
    # SECTION 5: QUEUE LENGTH OVER TIME
    # --------------------------------------------------

    st.divider()

    st.header("🚗 Queue Length Over Time")

    fig, ax = plt.subplots(figsize=(11, 4))

    for label, result in results.items():

        history = result["history"]

        ax.plot(
            history["time"] / 60,
            history["total_queue"].rolling(
                15,
                min_periods=1
            ).mean(),
            label=label
        )

    ax.set_xlabel("Time (minutes)")

    ax.set_ylabel("Queue Length (15-second rolling average)")

    ax.set_title("Fixed-Time vs Fuzzy Logic Traffic Queue")

    ax.legend()

    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

    plt.close(fig)


    # --------------------------------------------------
    # SECTION 6: GREEN LIGHT DECISIONS
    # --------------------------------------------------

    st.divider()

    st.header("🚦 Green-Light Decisions")

    phase_tables = []

    for label, result in results.items():

        frame = result["phases"].copy()

        frame["controller"] = label

        phase_tables.append(frame)

    phase_comparison = pd.concat(
        phase_tables,
        ignore_index=True
    )

    st.dataframe(
        phase_comparison,
        use_container_width=True
    )


    # --------------------------------------------------
    # SECTION 7: DOWNLOAD RESULTS
    # --------------------------------------------------

    st.divider()

    st.header("📥 Download Simulation Results")

    st.download_button(
        label="Download Comparison CSV",

        data=comparison.to_csv().encode("utf-8"),

        file_name="traffic_controller_comparison.csv",

        mime="text/csv"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Educational simulation only. "
    "Not suitable for controlling real-world traffic signals."
)