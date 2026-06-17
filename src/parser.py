import re

class Parser:
    def __init__(self):
        self.entries = []

    def parse_line(self, line: str) -> dict | None:
        """Parse une ligne de log, retourne un dict ou None si ligne invalide."""
        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+(\w+)\s+(.+)"
        match = re.match(pattern, line.strip())
        if not match:
            return None

        timestamp, level, service, message = match.groups()

         # Extraire latency depuis le message
        latency_match = re.search(r"latency=(\d+)ms", message)
        latency = int(latency_match.group(1)) if latency_match else None
        
        # Extraire user depuis le message
        user_match = re.search(r"user=(\w+)", message)
        user = user_match.group(1) if user_match else None

        return {
            "timestamp": timestamp,
            "level":     level.upper(),    # normalisation
            "service":   service,
            "message":   message.strip(),
            "user":      user,
            "latency_ms": latency
        }

    def parse_file(self, filepath: str) -> int:
        """Lit un fichier de logs, retourne le nombre d'entrées parsées."""
        n = len(self.entries)
        with open(filepath, "r") as f:
            for line in f:
                entry = self.parse_line(line)
                if entry is not None:        # on ignore les lignes invalides
                    self.entries.append(entry)
        
        return len(self.entries) - n  # nombre de nouvelles entrées parsées
    
    def get_entries(self) -> list[dict]:
        """Retourne la liste des entrées parsées."""
        return self.entries