import os
import re
from collections import defaultdict
import sys
#sys.path.append(os.path.abspath("../"))
from app.core.constants import STRACE_LOG_PREFIX


class ProcessTreeBuilder:
    def __init__(self, artifact_dir: str):
        self.artifact_dir = artifact_dir
        self.process_tree = defaultdict(list)
        self.execution_map = defaultdict(list)

    def build(self):
        for file in os.listdir(self.artifact_dir):
            if not file.startswith(STRACE_LOG_PREFIX):
                continue

            pid = file.split(".")[-1]
            path = os.path.join(self.artifact_dir, file)

            with open(path, "r", errors="ignore") as f:
                for line in f:

                    # fork / clone detection
                    fork_match = re.search(r'(fork|clone)\(.*\)\s+=\s+(\d+)', line)
                    if fork_match:
                        child_pid = fork_match.group(2)
                        self.process_tree[pid].append(child_pid)

                    # execve detection
                    exec_match = re.search(r'execve\("([^"]+)"', line)
                    if exec_match:
                        binary = exec_match.group(1)
                        self.execution_map[pid].append(binary)

        return {
            "process_tree": dict(self.process_tree),
            "execution_map": dict(self.execution_map)
        }