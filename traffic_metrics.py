
"""
Traffic Performance Metrics
Person 2 Contribution
"""

def calculate_metrics(waiting_times, queue_lengths, vehicles_passed):

    if not waiting_times:
        avg_waiting = 0
    else:
        avg_waiting = sum(waiting_times) / len(waiting_times)

    if not queue_lengths:
        avg_queue = 0
    else:
        avg_queue = sum(queue_lengths) / len(queue_lengths)

    total_vehicles = sum(vehicles_passed)

    return {
        "average_waiting_time": round(avg_waiting, 2),
        "average_queue_length": round(avg_queue, 2),
        "total_vehicles_passed": total_vehicles
    }


def compare_controllers(fixed_metrics, fuzzy_metrics):

    comparison = {}

    for metric in fixed_metrics:

        fixed = fixed_metrics[metric]
        fuzzy = fuzzy_metrics[metric]

        if fixed == 0:
            improvement = 0
        else:
            if metric == "total_vehicles_passed":
                improvement = ((fuzzy - fixed) / fixed) * 100
            else:
                improvement = ((fixed - fuzzy) / fixed) * 100

        comparison[metric] = {
            "fixed_time": fixed,
            "fuzzy_logic": fuzzy,
            "improvement_percentage": round(improvement, 2)
        }

    return comparison


def get_congestion_level(queue_length):

    if queue_length < 5:
        return "Low"

    elif queue_length < 15:
        return "Medium"

    else:
        return "High"
