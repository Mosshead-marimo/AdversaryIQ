import json
import os


class MitreAttackDatabase:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "mitre_attack_data", "enterprise-attack.json")

        if not os.path.isfile(data_path):
            raise FileNotFoundError("MITRE ATT&CK dataset not found.")

        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.techniques = {}
        self._index_techniques()

    def _index_techniques(self):
        for obj in self.data["objects"]:
            if obj.get("type") == "attack-pattern":
                external_refs = obj.get("external_references", [])
                technique_id = None

                for ref in external_refs:
                    if ref.get("source_name") == "mitre-attack":
                        technique_id = ref.get("external_id")

                if technique_id:
                    self.techniques[technique_id] = {
                        "name": obj.get("name"),
                        "description": obj.get("description"),
                        "kill_chain_phases": obj.get("kill_chain_phases", [])
                    }

    def get_technique(self, technique_id):
        return self.techniques.get(technique_id)

    def search_by_keyword(self, keyword):
        results = []
        keyword_lower = keyword.lower()

        for tech_id, data in self.techniques.items():
            if keyword_lower in data["name"].lower() or keyword_lower in data["description"].lower():
                results.append((tech_id, data))

        return results