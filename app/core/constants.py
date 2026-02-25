"""
Global constants for PyDetonator
"""

# -------------------------------
# Sandbox Limits
# -------------------------------

DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_MEMORY_LIMIT = "512m"
DEFAULT_PIDS_LIMIT = 64

# -------------------------------
# Risk Thresholds
# -------------------------------

BENIGN_THRESHOLD = 10
SUSPICIOUS_THRESHOLD = 30

# -------------------------------
# Behavior Scoring Weights
# -------------------------------

BEHAVIOR_WEIGHTS = {
    "process_execution": 2,
    "process_spawn": 5,
    "socket_creation": 5,
    "network_connection": 8,
    "sensitive_file_access": 10,
    "file_write": 4,
}

# -------------------------------
# Heuristic Severity Weights
# -------------------------------

HEURISTIC_SEVERITY_WEIGHTS = {
    "High": 20,
    "Medium": 10,
    "Low": 5,
}

# -------------------------------
# Suspicious Directories
# -------------------------------

SUSPICIOUS_DIRECTORIES = [
    "/tmp/",
    "/var/tmp/",
    "/dev/shm/",
]

# -------------------------------
# File Naming
# -------------------------------

STRACE_LOG_PREFIX = "strace.log"
REPORT_FILE_EXTENSION = ".json"

# -------------------------------
# MITRE
# -------------------------------

MITRE_ATTACK_SOURCE_NAME = "mitre-attack"
ATTACK_PATTERN_TYPE = "attack-pattern"

# -------------------------------
# IOC Patterns
# -------------------------------

IPV4_REGEX = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
FILE_PATH_REGEX = r"\"(/[^\"\s]+)\""

# -------------------------------
# Heuristic Types
# -------------------------------

HEURISTIC_TYPES = {
    "DROPPER": "Dropper Behavior",
    "FORK_STORM": "Mass Process Spawn",
    "TEMP_EXECUTION": "Temp Directory Execution",
    "NETWORK_AFTER_EXEC": "Network After Execution",
}