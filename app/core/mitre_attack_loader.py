import json
import os
import sys


#sys.path.append(os.path.abspath("../"))
from app.core.constants import ATTACK_PATTERN_TYPE, MITRE_ATTACK_SOURCE_NAME

class MitreAttackDatabase:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(
            base_path,
            "mitre_attack_data",
            "enterprise-attack.json"
        )

        if not os.path.isfile(data_path):
            raise FileNotFoundError(
                "MITRE ATT&CK dataset not found in core/mitre_attack_data/"
            )

        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.techniques = {}
        self._index_techniques()

    def _index_techniques(self):
        for obj in self.data.get("objects", []):
            if obj.get("type") != ATTACK_PATTERN_TYPE:
                continue

            technique_id = None

            for ref in obj.get("external_references", []):
                if ref.get("source_name") == MITRE_ATTACK_SOURCE_NAME:
                    technique_id = ref.get("external_id")

            if technique_id:
                self.techniques[technique_id] = {
                    "name": obj.get("name"),
                    "description": obj.get("description"),
                    "kill_chain_phases": obj.get("kill_chain_phases", [])
                }

    def get_technique(self, technique_id: str):
        return self.techniques.get(technique_id)

    def search_by_keyword(self, keyword: str):
        results = []
        keyword = keyword.lower()

        for tech_id, data in self.techniques.items():
            name = data["name"].lower()
            desc = (data["description"] or "").lower()

            if keyword in name or keyword in desc:
                results.append((tech_id, data))

        return results