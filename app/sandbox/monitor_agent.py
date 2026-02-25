import os
import json
import hashlib


def compute_sha256(path):
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def collect_metadata(sample_path):
    if not os.path.exists(sample_path):
        return {"error": "Sample not found"}

    return {
        "exists": True,
        "size": os.path.getsize(sample_path),
        "sha256": compute_sha256(sample_path)
    }


if __name__ == "__main__":
    sample_path = "/analysis/sample"
    metadata = collect_metadata(sample_path)

    with open("/analysis/logs/sample_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)