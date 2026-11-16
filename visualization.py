import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


def create_comparison_graph(fixed_metrics, fuzzy_metrics):

    metrics = [
        "Average Waiting Time",
        "Average Queue Length",
        "Vehicles Passed"
    ]

    fixed_values = [
        fixed_metrics["average_waiting_time"],
        fixed_metrics["average_queue_length"],
        fixed_metrics["total_vehicles_passed"]
    ]

    fuzzy_values = [
        fuzzy_metrics["average_waiting_time"],
        fuzzy_metrics["average_queue_length"],
        fuzzy_metrics["total_vehicles_passed"]
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for i in range(3):

        axes[i].bar(
            ["Fixed Time", "Fuzzy Logic"],
            [fixed_values[i], fuzzy_values[i]]
        )

        axes[i].set_title(metrics[i])
        axes[i].set_ylabel("Value")
        axes[i].grid(axis="y", alpha=0.3)

    plt.suptitle(
        "Fixed-Time vs Fuzzy Logic Traffic Controller",
        fontsize=14
    )

    plt.tight_layout()

    os.makedirs("results", exist_ok=True)

    plt.savefig(
        "results/controller_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


def create_waiting_time_graph(fixed_waiting, fuzzy_waiting):

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        ["Fixed Time", "Fuzzy Logic"],
        [fixed_waiting, fuzzy_waiting]
    )

    ax.set_title("Average Traffic Waiting Time")
    ax.set_ylabel("Waiting Time (seconds)")
    ax.grid(axis="y", alpha=0.3)

    os.makedirs("results", exist_ok=True)

    plt.savefig(
        "results/waiting_time.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


def create_queue_graph(fixed_queue, fuzzy_queue):

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        ["Fixed Time", "Fuzzy Logic"],
        [fixed_queue, fuzzy_queue]
    )

    ax.set_title("Average Traffic Queue Length")
    ax.set_ylabel("Number of Vehicles")
    ax.grid(axis="y", alpha=0.3)

    os.makedirs("results", exist_ok=True)

    plt.savefig(
        "results/queue_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)