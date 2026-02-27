import sys
#sys.path.append("../")

from app.monitoring.process_parser import ProcessTreeBuilder
from app.monitoring.timeline_builder import ExecutionTimelineBuilder
from app.monitoring.network_parser import NetworkParser
from app.monitoring.filesystem_parser import FileSystemParser
from app.analyzer.behavior_engine import BehaviorAnalyzer
from app.analyzer.ioc_extractor import IOCExtractor
from app.analyzer.mitre_mapper import MitreMapper
from app.analyzer.heuristics_engine import HeuristicsEngine
from app.analyzer.scoring_engine import ScoringEngine
from app.reporting.report_builder import ReportBuilder


class ExecutionEngine:
    def __init__(self, analysis_id, sample_path, artifact_dir):
        self.analysis_id = analysis_id
        self.sample_path = sample_path
        self.artifact_dir = artifact_dir

    def run(self):

        # Process Tree
        tree_builder = ProcessTreeBuilder(self.artifact_dir)
        process_data = tree_builder.build()

        # Timeline
        timeline_builder = ExecutionTimelineBuilder(self.artifact_dir)
        timeline = timeline_builder.build()

        # Network
        network_parser = NetworkParser(self.artifact_dir)
        ip_addresses = network_parser.parse()

        # Filesystem
        fs_parser = FileSystemParser(self.artifact_dir)
        filesystem_data = fs_parser.parse()

        # Behavior
        analyzer = BehaviorAnalyzer(self.artifact_dir)
        analyzer.load_strace_logs()
        behavior = analyzer.analyze()

        # IOCs
        ioc_extractor = IOCExtractor(analyzer.syscalls)
        iocs = ioc_extractor.extract()
        iocs["ip_addresses"] = ip_addresses
        iocs["filesystem"] = filesystem_data

        # MITRE
        mitre = MitreMapper(behavior)
        techniques = mitre.map()

        # Heuristics
        heuristics = HeuristicsEngine(behavior, process_data, timeline)
        flags = heuristics.run()

        # Scoring
        scorer = ScoringEngine(behavior)
        scorer.calculate()
        scorer.add_heuristic_penalty(flags)
        score = scorer.score
        classification = scorer.classify()

        # Report
        report_builder = ReportBuilder(self.analysis_id, self.sample_path)
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

        return {
            "analysis_id": self.analysis_id,
            "score": score,
            "classification": classification,
            "report_path": report_path
        }