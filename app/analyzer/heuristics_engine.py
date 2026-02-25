class HeuristicsEngine:
    def __init__(self, behavior, process_data, timeline):
        self.behavior = behavior
        self.process_tree = process_data.get("process_tree", {})
        self.execution_map = process_data.get("execution_map", {})
        self.timeline = timeline

        self.flags = []

    def detect_dropper_behavior(self):
        written_files = set()
        executed_files = set()

        for event in self.timeline:
            if event.get("type") == "write" and "target" in event:
                written_files.add(event["target"])

            if event.get("type") == "execve" and "target" in event:
                executed_files.add(event["target"])

        dropped_and_executed = written_files.intersection(executed_files)

        if dropped_and_executed:
            self.flags.append({
                "type": "Dropper Behavior",
                "severity": "High",
                "details": list(dropped_and_executed)
            })

    def detect_fork_storm(self):
        for parent, children in self.process_tree.items():
            if len(children) > 10:
                self.flags.append({
                    "type": "Mass Process Spawn",
                    "severity": "High",
                    "details": f"Parent PID {parent} spawned {len(children)} children"
                })

    def detect_temp_execution(self):
        for pid, binaries in self.execution_map.items():
            for binary in binaries:
                if "/tmp/" in binary or "/var/tmp/" in binary:
                    self.flags.append({
                        "type": "Temp Directory Execution",
                        "severity": "Medium",
                        "details": binary
                    })

    def detect_network_after_exec(self):
        exec_seen = False

        for event in self.timeline:
            if event.get("type") == "execve":
                exec_seen = True

            if exec_seen and event.get("type") == "connect":
                self.flags.append({
                    "type": "Network After Execution",
                    "severity": "High",
                    "details": "Process initiated network connection after execution"
                })
                break

    def run(self):
        self.detect_dropper_behavior()
        self.detect_fork_storm()
        self.detect_temp_execution()
        self.detect_network_after_exec()

        return self.flags