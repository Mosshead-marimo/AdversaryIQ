import re


class IOCExtractor:
    def __init__(self, syscalls: list):
        self.syscalls = syscalls
        self.iocs = {
            "ip_addresses": set(),
            "file_paths": set(),
        }

    def extract(self):
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        path_pattern = r'\"(/[^"]+)\"'

        for line in self.syscalls:
            ips = re.findall(ip_pattern, line)
            for ip in ips:
                self.iocs["ip_addresses"].add(ip)

            paths = re.findall(path_pattern, line)
            for path in paths:
                if len(path) > 3:
                    self.iocs["file_paths"].add(path)

        return {
            "ip_addresses": list(self.iocs["ip_addresses"]),
            "file_paths": list(self.iocs["file_paths"]),
        }