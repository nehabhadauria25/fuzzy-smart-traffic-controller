import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def build_fuzzy_system():
    """Define fuzzy inputs, output, membership functions and nine rules."""
    congestion = ctrl.Antecedent(np.arange(0, 41, 1), "congestion")
    waiting = ctrl.Antecedent(np.arange(0, 121, 1), "waiting")
    green = ctrl.Consequent(np.arange(10, 61, 1), "green")

    congestion["low"] = fuzz.trimf(congestion.universe, [0, 0, 20])
    congestion["medium"] = fuzz.trimf(congestion.universe, [10, 20, 30])
    congestion["high"] = fuzz.trimf(congestion.universe, [20, 40, 40])

    waiting["short"] = fuzz.trimf(waiting.universe, [0, 0, 60])
    waiting["moderate"] = fuzz.trimf(waiting.universe, [30, 60, 90])
    waiting["long"] = fuzz.trimf(waiting.universe, [60, 120, 120])

    green["short"] = fuzz.trimf(green.universe, [10, 10, 30])
    green["medium"] = fuzz.trimf(green.universe, [20, 35, 50])
    green["long"] = fuzz.trimf(green.universe, [40, 60, 60])

    rules = [
        ctrl.Rule(congestion["low"] & waiting["short"], green["short"]),
        ctrl.Rule(congestion["low"] & waiting["moderate"], green["short"]),
        ctrl.Rule(congestion["low"] & waiting["long"], green["medium"]),
        ctrl.Rule(congestion["medium"] & waiting["short"], green["medium"]),
        ctrl.Rule(congestion["medium"] & waiting["moderate"], green["medium"]),
        ctrl.Rule(congestion["medium"] & waiting["long"], green["long"]),
        ctrl.Rule(congestion["high"] & waiting["short"], green["medium"]),
        ctrl.Rule(congestion["high"] & waiting["moderate"], green["long"]),
        ctrl.Rule(congestion["high"] & waiting["long"], green["long"]),
    ]
    return ctrl.ControlSystem(rules)


_FUZZY_SYSTEM = build_fuzzy_system()


def fuzzy_controller(queue_length, waiting_time, fixed_green_seconds=30):
    """Choose green duration from queue size and oldest vehicle wait."""
    sim = ctrl.ControlSystemSimulation(_FUZZY_SYSTEM)
    sim.input["congestion"] = float(np.clip(queue_length, 0, 40))
    sim.input["waiting"] = float(np.clip(waiting_time, 0, 120))
    sim.compute()
    return int(round(sim.output["green"]))
