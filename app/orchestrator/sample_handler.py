import os
import uuid
import shutil
from app.core.config import SAMPLES_DIR, ARTIFACTS_DIR


class SampleHandler:
    def __init__(self, sample_path: str):
        self.original_path = sample_path
        self.analysis_id = str(uuid.uuid4())
        self.sample_path = None
        self.artifact_dir = None

    def prepare(self):
        if not os.path.isfile(self.original_path):
            raise FileNotFoundError("Sample file not found")

        filename = os.path.basename(self.original_path)
        safe_name = f"{self.analysis_id}_{filename}"

        self.sample_path = os.path.join(SAMPLES_DIR, safe_name)
        shutil.copy2(self.original_path, self.sample_path)

        self.artifact_dir = os.path.join(ARTIFACTS_DIR, self.analysis_id)
        os.makedirs(self.artifact_dir, exist_ok=True)

        return {
            "analysis_id": self.analysis_id,
            "sample_path": self.sample_path,
            "artifact_dir": self.artifact_dir
        }
