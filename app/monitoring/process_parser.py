import os
import re
from collections import defaultdict


class ProcessTreeBuilder:
    def __init__(self, artifact_dir: str):
        self.artifact_dir = artifact_dir
        self.process_tree = defaultdict(list)
        self.exec_events = defaultdict(list)

    def build(self):
        for file in os.listdir(self.artifact_dir):
            if not file.startswith("strace.log"):
                continue

            pid = file.split(".")[-1]
            path = os.path.join(self.artifact_dir, file)

            with open(path, "r", errors="ignore") as f:
                lines = f.readlines()

            for line in lines:
                # Detect fork/clone
                fork_match = re.search(r'(fork|clone)\(.*\)\s+=\s+(\d+)', line)
                if fork_match:
                    child_pid = fork_match.group(2)
                    self.process_tree[pid].append(child_pid)

                # Detect execve
                exec_match = re.search(r'execve\("([^"]+)"', line)
                if exec_match:
                    executed_binary = exec_match.group(1)
                    self.exec_events[pid].append(executed_binary)

        return {
            "process_tree": dict(self.process_tree),
            "execution_map": dict(self.exec_events)
        }