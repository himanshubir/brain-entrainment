from config import HYSTERESIS_THRESHOLD

class BrainStateDetector:
    def __init__(self):
        self.previous_state = None
        self.previous_powers = {}

    def detect_state(self, power_dict):
        total = sum(power_dict[band] for band in ['delta', 'theta', 'alpha', 'beta', 'gamma'])

        rel_powers = {
            'DELTA': power_dict['delta'] / total,
            'THETA': power_dict['theta'] / total,
            'ALPHA': power_dict['alpha'] / total,
            'BETA': power_dict['beta'] / total,
            'GAMMA': power_dict['gamma'] / total
        }

        candidate = max(rel_powers, key=rel_powers.get)

        # if self.previous_state and candidate != self.previous_state:
        #     threshold = self.previous_powers[self.previous_state] * (1 + HYSTERESIS_THRESHOLD)
        #     if rel_powers[candidate] < threshold:
        #         return self.previous_state

        self.previous_state = candidate
        self.previous_powers = rel_powers
        return candidate
