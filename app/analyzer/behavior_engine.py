import os
import re
from collections import defaultdict


class BehaviorAnalyzer:
    def __init__(self, artifact_dir: str):
        self.artifact_dir = artifact_dir
        self.syscalls = []
        self.behavior = defaultdict(int)

    def load_strace_logs(self):
        for file in os.listdir(self.artifact_dir):
            if file.startswith("strace.log"):
                path = os.path.join(self.artifact_dir, file)
                with open(path, "r", errors="ignore") as f:
                    self.syscalls.extend(f.readlines())

    def analyze(self):
        for line in self.syscalls:
            if "execve(" in line:
                self.behavior["process_execution"] += 1

            if "fork(" in line or "clone(" in line:
                self.behavior["process_spawn"] += 1

            if "socket(" in line:
                self.behavior["socket_creation"] += 1

            if "connect(" in line:
                self.behavior["network_connection"] += 1

            if re.search(r'open(at)?\(.*/etc/', line):
                self.behavior["sensitive_file_access"] += 1

            if "write(" in line:
                self.behavior["file_write"] += 1

        return dict(self.behavior)