import sys
import os

sys.path.append(os.path.abspath("../"))

from docker_manager import DockerSandboxManager
from analyzer.behavior_engine import BehaviorAnalyzer
from analyzer.scoring_engine import ScoringEngine
from analyzer.ioc_extractor import IOCExtractor
from reporting.report_builder import ReportBuilder


sample_path = os.path.abspath("../../test.sh")

manager = DockerSandboxManager(timeout=20)
result = manager.analyze_sample(sample_path)

analysis_id = result["analysis_id"]
artifact_dir = result["artifact_dir"]

print("Analysis ID:", analysis_id)

analyzer = BehaviorAnalyzer(artifact_dir)
analyzer.load_strace_logs()
behavior = analyzer.analyze()

scorer = ScoringEngine(behavior)
score = scorer.calculate()
classification = scorer.classify()

ioc_extractor = IOCExtractor(analyzer.syscalls)
iocs = ioc_extractor.extract()

report_builder = ReportBuilder(analysis_id, sample_path)
report_path = report_builder.build(behavior, score, classification, iocs)

print("Score:", score)
print("Classification:", classification)
print("Report saved at:", report_path)