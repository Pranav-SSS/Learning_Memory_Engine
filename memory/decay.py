import math

def apply_spaced_decay(mastery, days_passed, stability):
    if stability <= 0:
        stability = 1.0
    return mastery * math.exp(-days_passed / stability)


def update_stability(stability, correct):
    if correct:
        return stability * 1.3
    return max(1.0, stability * 0.9)