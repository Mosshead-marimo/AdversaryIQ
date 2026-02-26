import os
import re
from app.core.constants import STRACE_LOG_PREFIX


class ExecutionTimelineBuilder:
    def __init__(self, artifact_dir: str):
        self.artifact_dir = artifact_dir
        self.events = []

    def _parse_line(self, pid, line):
        event = {
            "pid": pid,
            "raw": line.strip()
        }

        # Timestamp parsing (if -tt enabled)
        timestamp_match = re.match(r"(\d+:\d+:\d+\.\d+)", line)
        if timestamp_match:
            event["timestamp"] = timestamp_match.group(1)

        if "execve(" in line:
            match = re.search(r'execve\("([^"]+)"', line)
            if match:
                event["type"] = "execve"
                event["target"] = match.group(1)

        elif "connect(" in line:
            event["type"] = "connect"

        elif "write(" in line:
            event["type"] = "write"

        elif "open(" in line or "openat(" in line:
            event["type"] = "file_open"

        else:
            return None

        return event

    def build(self):
        for file in os.listdir(self.artifact_dir):
            if not file.startswith(STRACE_LOG_PREFIX):
                continue

            pid = file.split(".")[-1]
            path = os.path.join(self.artifact_dir, file)

            with open(path, "r", errors="ignore") as f:
                for line in f:
                    event = self._parse_line(pid, line)
                    if event:
                        self.events.append(event)

        return self.events
