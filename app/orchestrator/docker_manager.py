import os
import uuid
import shutil
import docker
import time


class DockerSandboxManager:
    def __init__(self, image_name="pydetonator-sandbox", timeout=30):
        self.client = docker.from_env()
        self.image_name = image_name
        self.timeout = timeout

    def analyze_sample(self, sample_path: str) -> dict:
        if not os.path.isfile(sample_path):
            raise FileNotFoundError(f"Sample not found: {sample_path}")

        analysis_id = str(uuid.uuid4())
        artifact_dir = os.path.abspath(os.path.join("artifacts", analysis_id))
        os.makedirs(artifact_dir, exist_ok=True)

        container = None

        try:
            container = self.client.containers.run(
                self.image_name,
                detach=True,
                volumes={
                    os.path.abspath(sample_path): {
                        "bind": "/analysis/sample",
                        "mode": "ro",
                    },
                    artifact_dir: {
                        "bind": "/analysis/logs",
                        "mode": "rw",
                    },
                },
                mem_limit="512m",
                pids_limit=64,
                read_only=True,
                cap_drop=["ALL"],
                network_mode="bridge",
                security_opt=["no-new-privileges"],
            )

            start_time = time.time()

            while True:
                container.reload()
                if container.status in ["exited", "dead"]:
                    break

                if time.time() - start_time > self.timeout:
                    container.kill()
                    break

                time.sleep(1)

            logs = container.logs().decode(errors="ignore")

        finally:
            if container:
                container.remove(force=True)

        return {
            "analysis_id": analysis_id,
            "artifact_dir": artifact_dir,
            "container_logs": logs,
        }