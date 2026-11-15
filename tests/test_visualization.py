
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from visualization import (
    create_comparison_graph,
    create_waiting_time_graph,
    create_queue_graph
)


def test_comparison_graph():

    fixed = {
        "average_waiting_time": 40,
        "average_queue_length": 20,
        "total_vehicles_passed": 100
    }

    fuzzy = {
        "average_waiting_time": 20,
        "average_queue_length": 10,
        "total_vehicles_passed": 150
    }

    create_comparison_graph(fixed, fuzzy)

    assert os.path.exists(
        "results/controller_comparison.png"
    )


def test_waiting_time_graph():

    create_waiting_time_graph(40, 20)

    assert os.path.exists(
        "results/waiting_time.png"
    )


def test_queue_graph():

    create_queue_graph(20, 10)

    assert os.path.exists(
        "results/queue_comparison.png"
    )
