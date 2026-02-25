import os
import uuid
import shutil
import sys
from fastapi import APIRouter, UploadFile, File, HTTPException
sys.path.append(os.path.abspath("../"))
from orchestrator.docker_manager import DockerSandboxManager
from analyzer.behavior_engine import BehaviorAnalyzer
from analyzer.scoring_engine import ScoringEngine
from analyzer.ioc_extractor import IOCExtractor
from analyzer.mitre_mapper import MitreMapper
from analyzer.heuristics_engine import HeuristicsEngine
from monitoring.process_parser import ProcessTreeBuilder
from monitoring.timeline_builder import ExecutionTimelineBuilder
from reporting.report_builder import ReportBuilder

router = APIRouter()

UPLOAD_DIR = os.path.abspath("samples")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze")
async def analyze_sample(file: UploadFile = File(...)):
    analysis_id = str(uuid.uuid4())
    sample_path = os.path.join(UPLOAD_DIR, f"{analysis_id}_{file.filename}")

    try:
        with open(sample_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        manager = DockerSandboxManager(timeout=20)
        result = manager.analyze_sample(sample_path)

        artifact_dir = result["artifact_dir"]

        # Process Tree
        tree_builder = ProcessTreeBuilder(artifact_dir)
        process_data = tree_builder.build()

        # Timeline
        timeline_builder = ExecutionTimelineBuilder(artifact_dir)
        timeline = timeline_builder.build()

        # Behavior
        analyzer = BehaviorAnalyzer(artifact_dir)
        analyzer.load_strace_logs()
        behavior = analyzer.analyze()

        # IOCs
        ioc_extractor = IOCExtractor(analyzer.syscalls)
        iocs = ioc_extractor.extract()

        # MITRE
        mitre = MitreMapper(behavior)
        techniques = mitre.map()

        # Heuristics
        heuristics = HeuristicsEngine(behavior, process_data, timeline)
        flags = heuristics.run()

        # Scoring
        scorer = ScoringEngine(behavior)
        score = scorer.calculate()
        scorer.add_heuristic_penalty(flags)
        score = scorer.score
        classification = scorer.classify()

        # Report
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

        return {
            "analysis_id": analysis_id,
            "status": "completed"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))