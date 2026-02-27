import os
import re
import sys
#sys.path.append(os.path.abspath("../"))
from app.core.constants import IPV4_REGEX, STRACE_LOG_PREFIX


class NetworkParser:
    def __init__(self, artifact_dir: str):
        self.artifact_dir = artifact_dir
        self.ip_addresses = set()

    def parse(self):
        for file in os.listdir(self.artifact_dir):
            if not file.startswith(STRACE_LOG_PREFIX):
                continue

            with open(os.path.join(self.artifact_dir, file), "r", errors="ignore") as f:
                for line in f:
                    if "connect(" in line:
                        ips = re.findall(IPV4_REGEX, line)
                        for ip in ips:
                            self.ip_addresses.add(ip)

        return list(self.ip_addresses)