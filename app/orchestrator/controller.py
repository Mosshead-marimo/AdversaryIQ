from app.orchestrator.sample_handler import SampleHandler
from app.orchestrator.docker_manager import DockerSandboxManager
from app.orchestrator.execution_engine import ExecutionEngine


class AnalysisController:
    def __init__(self, sample_path: str):
        self.sample_path = sample_path

    def run(self):
        # Prepare sample
        handler = SampleHandler(self.sample_path)
        prepared = handler.prepare()

        analysis_id = prepared["analysis_id"]
        sample_path = prepared["sample_path"]
        artifact_dir = prepared["artifact_dir"]

        # Execute sandbox
        sandbox = DockerSandboxManager()
        sandbox.execute(sample_path, artifact_dir)

        # Run full analysis pipeline
        engine = ExecutionEngine(
            analysis_id,
            sample_path,
            artifact_dir
        )

        result = engine.run()

        return result
