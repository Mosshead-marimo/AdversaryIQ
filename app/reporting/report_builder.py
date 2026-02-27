import os
import json
import hashlib
from datetime import datetime
import sys
#sys.path.append(os.path.abspath("../"))
from app.core.config import REPORTS_DIR
from app.core.constants import REPORT_FILE_EXTENSION


class ReportBuilder:
    def __init__(self, analysis_id: str, sample_path: str):
        self.analysis_id = analysis_id
        self.sample_path = sample_path
        self.report_dir = REPORTS_DIR
        os.makedirs(self.report_dir, exist_ok=True)

    # --------------------------------------------------
    # Utility: Compute SHA256
    # --------------------------------------------------

    def _compute_hash(self):
        sha256 = hashlib.sha256()
        with open(self.sample_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    # --------------------------------------------------
    # Aggregate MITRE Tactics
    # --------------------------------------------------

    def _aggregate_tactics(self, techniques):
        tactic_counter = {}

        for technique in techniques:
            phases = technique.get("kill_chain_phases", [])
            for phase in phases:
                tactic = phase.get("phase_name")
                if tactic:
                    tactic_counter[tactic] = tactic_counter.get(tactic, 0) + 1

        return tactic_counter

    # --------------------------------------------------
    # Aggregate Technique Summary
    # --------------------------------------------------

    def _aggregate_techniques(self, techniques):
        technique_summary = {}

        for technique in techniques:
            tech_id = technique["technique_id"]
            technique_summary[tech_id] = {
                "name": technique["technique_name"],
                "evidence_count": technique["evidence_count"]
            }

        return technique_summary

    # --------------------------------------------------
    # Build JSON Report
    # --------------------------------------------------

    def build(
        self,
        behavior,
        score,
        classification,
        iocs,
        techniques,
        timeline,
        process_data,
        flags
    ):
        sha256_hash = self._compute_hash()

        tactic_summary = self._aggregate_tactics(techniques)
        technique_summary = self._aggregate_techniques(techniques)

        report = {
            "analysis_metadata": {
                "analysis_id": self.analysis_id,
                "timestamp_utc": datetime.utcnow().isoformat(),
                "engine": "PyDetonator",
                "version": "1.0"
            },
            "sample_information": {
                "original_path": os.path.abspath(self.sample_path),
                "sha256": sha256_hash,
                "file_size_bytes": os.path.getsize(self.sample_path)
            },
            "risk_assessment": {
                "risk_score": score,
                "classification": classification
            },
            "behavior_summary": behavior,
            "mitre_attack_analysis": {
                "mapped_techniques": techniques,
                "technique_count": len(techniques),
                "technique_summary": technique_summary,
                "tactic_distribution": tactic_summary
            },
            "advanced_behavior_analysis": {
                "process_tree": process_data.get("process_tree", {}),
                "execution_map": process_data.get("execution_map", {}),
                "execution_timeline": timeline,
                "heuristic_flags": flags
            },
            "indicators_of_compromise": iocs
        }

        report_path = os.path.join(
            self.report_dir,
            f"{self.analysis_id}{REPORT_FILE_EXTENSION}"
        )

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        return report_path