class ScoringEngine:
    def __init__(self, behavior: dict):
        self.behavior = behavior
        self.score = 0

    def calculate(self):
        weights = {
            "process_execution": 2,
            "process_spawn": 5,
            "socket_creation": 5,
            "network_connection": 8,
            "sensitive_file_access": 10,
            "file_write": 4,
        }

        for key, value in self.behavior.items():
            if key in weights:
                self.score += weights[key] * value

        return self.score

    def classify(self):
        if self.score < 10:
            return "Benign"
        elif self.score < 25:
            return "Suspicious"
        else:
            return "Malicious"