import sys
import os

sys.path.append(os.path.abspath("../"))

from docker_manager import DockerSandboxManager
from analyzer.behavior_engine import BehaviorAnalyzer
from analyzer.scoring_engine import ScoringEngine
from analyzer.ioc_extractor import IOCExtractor
from analyzer.mitre_mapper import MitreMapper
from analyzer.heuristics_engine import HeuristicsEngine
from reporting.report_builder import ReportBuilder
from monitoring.process_parser import ProcessTreeBuilder
from monitoring.timeline_builder import ExecutionTimelineBuilder


# ----------- CONFIG -----------

sample_path = os.path.abspath("../../test.sh")

# ----------- EXECUTION ENGINE -----------

manager = DockerSandboxManager(timeout=20)
result = manager.analyze_sample(sample_path)

analysis_id = result["analysis_id"]
artifact_dir = result["artifact_dir"]

print("Analysis ID:", analysis_id)

# ----------- PROCESS TREE -----------

tree_builder = ProcessTreeBuilder(artifact_dir)
process_data = tree_builder.build()

print("Process Tree:", process_data["process_tree"])
print("Execution Map:", process_data["execution_map"])

# ----------- TIMELINE -----------

timeline_builder = ExecutionTimelineBuilder(artifact_dir)
timeline = timeline_builder.build()

print("Execution Timeline:")
for event in timeline:
    print(event)

# ----------- BEHAVIOR ANALYSIS -----------

analyzer = BehaviorAnalyzer(artifact_dir)
analyzer.load_strace_logs()
behavior = analyzer.analyze()

# ----------- IOC EXTRACTION -----------

ioc_extractor = IOCExtractor(analyzer.syscalls)
iocs = ioc_extractor.extract()

# ----------- MITRE MAPPING -----------

mitre = MitreMapper(behavior)
techniques = mitre.map()

# ----------- HEURISTICS ENGINE -----------

heuristics = HeuristicsEngine(behavior, process_data, timeline)
flags = heuristics.run()

print("Heuristic Flags:", flags)

# ----------- SCORING -----------

scorer = ScoringEngine(behavior)
score = scorer.calculate()

# Apply heuristic penalties
scorer.add_heuristic_penalty(flags)
score = scorer.score

classification = scorer.classify()

# ----------- REPORT GENERATION -----------

report_builder = ReportBuilder(analysis_id, sample_path)
report_path = report_builder.build(
    behavior,
    score,
    classification,
    iocs,
    techniques,
    timeline,
    process_data,
    flags
)

print("Final Score:", score)
print("Classification:", classification)
print("Report saved at:", report_path)