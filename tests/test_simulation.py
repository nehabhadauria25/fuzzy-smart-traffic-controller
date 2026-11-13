
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from traffic_metrics import (
    calculate_metrics,
    compare_controllers,
    get_congestion_level
)


def test_calculate_metrics():

    result = calculate_metrics(
        [10, 20, 30],
        [5, 10, 15],
        [10, 20, 30]
    )

    assert result["average_waiting_time"] == 20
    assert result["average_queue_length"] == 10
    assert result["total_vehicles_passed"] == 60


def test_compare_controllers():

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

    result = compare_controllers(fixed, fuzzy)

    assert result["average_waiting_time"]["improvement_percentage"] == 50

    assert result["total_vehicles_passed"]["improvement_percentage"] == 50


def test_congestion_level():

    assert get_congestion_level(3) == "Low"

    assert get_congestion_level(10) == "Medium"

    assert get_congestion_level(20) == "High"
