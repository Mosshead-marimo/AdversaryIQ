import os
import uuid
import time
import docker
from core.config import ARTIFACTS_DIR, DOCKER_IMAGE


class DockerSandboxManager:
    def __init__(self, image_name=DOCKER_IMAGE, timeout=30):
        self.client = docker.DockerClient(
            base_url="npipe:////./pipe/docker_engine"
        )
        self.client.ping()

        self.image_name = image_name
        self.timeout = timeout

    def analyze_sample(self, sample_path: str):
        if not os.path.isfile(sample_path):
            raise FileNotFoundError("Sample not found")

        analysis_id = str(uuid.uuid4())
        artifact_dir = os.path.join(ARTIFACTS_DIR, analysis_id)
        os.makedirs(artifact_dir, exist_ok=True)

        container = None

        try:
            container = self.client.containers.run(
                self.image_name,
                detach=True,
                volumes={
                    sample_path: {
                        "bind": "/analysis/sample",
                        "mode": "ro"
                    },
                    artifact_dir: {
                        "bind": "/analysis/logs",
                        "mode": "rw"
                    }
                },
                mem_limit="512m",
                pids_limit=64,
                read_only=True,
                cap_drop=["ALL"],
                security_opt=["no-new-privileges"]
            )

            start = time.time()

            while True:
                container.reload()

                if container.status in ["exited", "dead"]:
                    break

                if time.time() - start > self.timeout:
                    container.kill()
                    break

                time.sleep(1)

        finally:
            if container:
                container.remove(force=True)

        return {
            "analysis_id": analysis_id,
            "artifact_dir": artifact_dir
        }