import os
import re
import sys
sys.path.append(os.path.abspath("../"))
from core.constants import STRACE_LOG_PREFIX


class SyscallParser:
    def __init__(self, artifact_dir: str):
        self.artifact_dir = artifact_dir
        self.syscalls = []

    def parse(self):
        for file in os.listdir(self.artifact_dir):
            if not file.startswith(STRACE_LOG_PREFIX):
                continue

            pid = file.split(".")[-1]

            with open(os.path.join(self.artifact_dir, file), "r", errors="ignore") as f:
                for line in f:
                    match = re.match(r"(\w+)\(", line.strip())
                    if match:
                        syscall_name = match.group(1)

                        self.syscalls.append({
                            "pid": pid,
                            "syscall": syscall_name,
                            "raw": line.strip()
                        })

        return self.syscalls