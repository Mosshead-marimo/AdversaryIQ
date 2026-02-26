import os
import time
import docker
import sys
sys.path.append(os.path.abspath("../"))
from core.config import DOCKER_IMAGE
from core.constants import DEFAULT_TIMEOUT_SECONDS, DEFAULT_MEMORY_LIMIT, DEFAULT_PIDS_LIMIT


class DockerSandboxManager:
    def __init__(self, image_name=DOCKER_IMAGE, timeout=DEFAULT_TIMEOUT_SECONDS):
        docker_host = os.getenv("DOCKER_HOST")
        if docker_host:
            self.client = docker.DockerClient(base_url=docker_host)
        else:
            self.client = docker.from_env()
        self.client.ping()

        self.image_name = image_name
        self.timeout = timeout

    def execute(self, sample_path: str, artifact_dir: str):
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
                mem_limit=DEFAULT_MEMORY_LIMIT,
                pids_limit=DEFAULT_PIDS_LIMIT,
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
