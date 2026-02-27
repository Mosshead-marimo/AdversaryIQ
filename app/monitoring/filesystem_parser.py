import os
import re
import sys
#sys.path.append(os.path.abspath("../"))
from app.core.constants import FILE_PATH_REGEX, STRACE_LOG_PREFIX


class FileSystemParser:
    def __init__(self, artifact_dir: str):
        self.artifact_dir = artifact_dir
        self.files_accessed = set()
        self.files_written = set()

    def parse(self):
        for file in os.listdir(self.artifact_dir):
            if not file.startswith(STRACE_LOG_PREFIX):
                continue

            with open(os.path.join(self.artifact_dir, file), "r", errors="ignore") as f:
                for line in f:
                    match = re.search(FILE_PATH_REGEX, line)
                    if match:
                        path = match.group(1)

                        if "write(" in line:
                            self.files_written.add(path)
                        elif "open(" in line or "openat(" in line:
                            self.files_accessed.add(path)

        return {
            "files_accessed": list(self.files_accessed),
            "files_written": list(self.files_written)
        }