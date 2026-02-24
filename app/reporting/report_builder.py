import os
import json
import hashlib
from datetime import datetime


class ReportBuilder:
    def __init__(self, analysis_id: str, sample_path: str):
        self.analysis_id = analysis_id
        self.sample_path = sample_path
        self.report_dir = os.path.abspath("reports")
        os.makedirs(self.report_dir, exist_ok=True)

    def _compute_hash(self):
        sha256 = hashlib.sha256()
        with open(self.sample_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _aggregate_tactics(self, techniques):
        tactic_counter = {}

        for technique in techniques:
            phases = technique.get("kill_chain_phases", [])
            for phase in phases:
                tactic = phase.get("phase_name")
                if tactic:
                    tactic_counter[tactic] = tactic_counter.get(tactic, 0) + 1

        return tactic_counter

    def _aggregate_techniques(self, techniques):
        technique_summary = {}

        for technique in techniques:
            tech_id = technique["technique_id"]
            technique_summary[tech_id] = {
                "name": technique["technique_name"],
                "evidence_count": technique["evidence_count"]
            }

        return technique_summary

    def build(
        self,
        behavior: dict,
        score: int,
        classification: str,
        iocs: dict,
        techniques: list
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
                "path": os.path.abspath(self.sample_path),
                "sha256": sha256_hash,
                "file_size_bytes": os.path.getsize(self.sample_path)
            },
            "behavior_summary": behavior,
            "risk_assessment": {
                "risk_score": score,
                "classification": classification
            },
            "mitre_attack_analysis": {
                "mapped_techniques": techniques,
                "technique_count": len(techniques),
                "technique_summary": technique_summary,
                "tactic_distribution": tactic_summary
            },
            "indicators_of_compromise": iocs
        }

        report_path = os.path.join(self.report_dir, f"{self.analysis_id}.json")

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        return report_path