import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

DOCKER_IMAGE = "pydetonator-sandbox:latest"

# Ensure directories exist
os.makedirs(SAMPLES_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)