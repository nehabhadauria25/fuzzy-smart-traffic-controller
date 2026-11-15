
"""
Traffic Visualization Module
Person 3 Contribution
"""

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

    plt.show()


def create_waiting_time_graph(fixed_waiting, fuzzy_waiting):

    plt.figure(figsize=(8, 5))

    plt.bar(
        ["Fixed Time", "Fuzzy Logic"],
        [fixed_waiting, fuzzy_waiting]
    )

    plt.title("Average Traffic Waiting Time")

    plt.ylabel("Waiting Time (seconds)")

    plt.grid(axis="y", alpha=0.3)

    os.makedirs("results", exist_ok=True)

    plt.savefig(
        "results/waiting_time.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


def create_queue_graph(fixed_queue, fuzzy_queue):

    plt.figure(figsize=(8, 5))

    plt.bar(
        ["Fixed Time", "Fuzzy Logic"],
        [fixed_queue, fuzzy_queue]
    )

    plt.title("Average Traffic Queue Length")

    plt.ylabel("Number of Vehicles")

    plt.grid(axis="y", alpha=0.3)

    os.makedirs("results", exist_ok=True)

    plt.savefig(
        "results/queue_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

