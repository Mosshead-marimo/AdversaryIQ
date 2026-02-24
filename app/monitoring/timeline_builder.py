import os
import re
from datetime import datetime


class ExecutionTimelineBuilder:
    def __init__(self, artifact_dir: str):
        self.artifact_dir = artifact_dir
        self.events = []

    def _parse_line(self, pid, line):
        # strace with default format doesn't include absolute timestamps
        # but includes relative timing if -tt is used.
        # We'll support basic parsing for now.

        event = {
            "pid": pid,
            "raw": line.strip()
        }

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
            if not file.startswith("strace.log"):
                continue

            pid = file.split(".")[-1]
            path = os.path.join(self.artifact_dir, file)

            with open(path, "r", errors="ignore") as f:
                for line in f:
                    event = self._parse_line(pid, line)
                    if event:
                        self.events.append(event)

        # Since we don’t yet use -tt, we keep insertion order
        return self.events
    def detect_staged_execution(self):
        written_files = set()
        staged = []

        for event in self.events:
            if event.get("type") == "write":
                written_files.add(event.get("target"))

            if event.get("type") == "execve":
              if event.get("target") in written_files:
                staged.append(event.get("target"))

        return staged