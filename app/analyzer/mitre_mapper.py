from core.mitre_attack_loader import MitreAttackDatabase


class MitreMapper:
    def __init__(self, behavior: dict):
        self.behavior = behavior
        self.db = MitreAttackDatabase()

    def map(self):
        mapped = []

        behavior_to_keywords = {
            "process_execution": ["command", "script", "execution"],
            "process_spawn": ["process injection", "spawn", "fork"],
            "socket_creation": ["network", "socket"],
            "network_connection": ["command and control", "c2", "exfiltration"],
            "sensitive_file_access": ["credential", "password", "dump"],
            "file_write": ["persistence", "dropper", "file transfer"],
        }

        for behavior_key, count in self.behavior.items():
            if count <= 0:
                continue

            keywords = behavior_to_keywords.get(behavior_key, [])
            for keyword in keywords:
                matches = self.db.search_by_keyword(keyword)

                for tech_id, data in matches:
                    mapped.append({
                        "technique_id": tech_id,
                        "technique_name": data["name"],
                        "kill_chain_phases": data["kill_chain_phases"],
                        "evidence_count": count
                    })

        # Remove duplicates
        unique = {m["technique_id"]: m for m in mapped}
        return list(unique.values())