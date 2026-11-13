from collections import deque
import numpy as np
import pandas as pd


# Generate vehicle arrivals
def generate_arrivals(
    simulation_seconds=600,
    ns_rate=0.35,
    ew_rate=0.30,
    seed=42
):
    rng = np.random.default_rng(seed)

    arrivals = {
        "NS": rng.poisson(ns_rate, simulation_seconds),
        "EW": rng.poisson(ew_rate, simulation_seconds)
    }

    return arrivals


# Fixed-time traffic controller
def fixed_controller(
    queue_length,
    waiting_time,
    fixed_green_seconds=30
):
    return int(fixed_green_seconds)


# Main traffic simulation
def simulate_traffic(
    controller,
    arrivals,
    simulation_seconds=600,
    fixed_green_seconds=30,
    service_interval=2
):

    queues = {
        "NS": deque(),
        "EW": deque()
    }

    directions = ["NS", "EW"]

    phase_index = 0
    current_time = 0
    next_service_time = 0

    waiting_times = []
    history = []
    phase_history = []

    while current_time < simulation_seconds:

        direction = directions[phase_index]

        active_queue = queues[direction]

        if active_queue:
            oldest_wait = current_time - active_queue[0]
        else:
            oldest_wait = 0

        # Ask controller for green-light duration
        green_time = controller(
            len(active_queue),
            oldest_wait,
            fixed_green_seconds
        )

        green_time = int(np.clip(green_time, 10, 60))

        phase_history.append({
            "start_time": current_time,
            "direction": direction,
            "queue_at_start": len(active_queue),
            "oldest_wait_at_start": oldest_wait,
            "green_seconds": green_time
        })

        phase_end = min(
            current_time + green_time,
            simulation_seconds
        )

        while current_time < phase_end:

            # Add newly arriving vehicles
            for approach in directions:

                new_vehicles = int(
                    arrivals[approach][current_time]
                )

                for _ in range(new_vehicles):
                    queues[approach].append(current_time)

            # Allow vehicles to cross during green signal
            if (
                current_time >= next_service_time
                and queues[direction]
            ):

                arrival_time = queues[direction].popleft()

                waiting_times.append(
                    current_time - arrival_time
                )

                next_service_time = (
                    current_time + service_interval
                )

            total_queue = (
                len(queues["NS"]) + len(queues["EW"])
            )

            history.append({
                "time": current_time,
                "active_direction": direction,
                "NS_queue": len(queues["NS"]),
                "EW_queue": len(queues["EW"]),
                "total_queue": total_queue,
                "vehicles_crossed": len(waiting_times)
            })

            current_time += 1

        # Switch traffic direction
        phase_index = (phase_index + 1) % 2

    # Calculate performance metrics
    total_arrived = int(
        sum(np.sum(arrivals[d]) for d in directions)
    )

    total_crossed = len(waiting_times)

    average_waiting = (
        float(np.mean(waiting_times))
        if waiting_times else 0
    )

    maximum_waiting = (
        int(max(waiting_times))
        if waiting_times else 0
    )

    average_queue = (
        float(np.mean([
            row["total_queue"] for row in history
        ]))
        if history else 0
    )

    remaining_vehicles = (
        len(queues["NS"]) + len(queues["EW"])
    )

    metrics = {
        "Total vehicles arrived": total_arrived,
        "Vehicles crossed": total_crossed,
        "Average waiting time (sec)": round(
            average_waiting, 2
        ),
        "Maximum waiting time (sec)": maximum_waiting,
        "Average queue length": round(
            average_queue, 2
        ),
        "Vehicles still waiting": remaining_vehicles,
        "Throughput (vehicles/min)": round(
            total_crossed / (simulation_seconds / 60), 2
        )
    }

    return {
        "metrics": metrics,
        "history": pd.DataFrame(history),
        "phases": pd.DataFrame(phase_history),
        "wait_times": waiting_times
    }