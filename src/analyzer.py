class Analyzer:
    def count_by_service(self, entries: list[dict]) -> dict:
        """
        Compte le d'entrées par service et par level.
        Retourne un dictionnaire avec le nom du service comme clé et le nombre d'entrées par level comme valeur.
        """
        res = dict()
        for entry in entries:
            service = entry["service"]
            level = entry["level"]
            if service not in res:
                res[service] = {}

            res[service][level] = res[service].get(level, 0) + 1

        return res

    def latency_stats_by_service(self, entries: list[dict]) -> dict:
        """
        Calcule les statistiques de latence par service.
        Retourne un dictionnaire avec la moyenne, le minimum et le maximum de latence pour chaque service.
        """
        stats = {}
        for entry in entries:
            service = entry["service"]
            latency = entry.get("latency_ms")
            if latency is not None:
                if service not in stats:
                    stats[service] = {"count": 0, "total_latency": 0, "min_latency": latency, "max_latency": latency}
                stats[service]["count"] += 1
                stats[service]["total_latency"] += latency
                stats[service]["min_latency"] = min(stats[service]["min_latency"], latency)
                stats[service]["max_latency"] = max(stats[service]["max_latency"], latency)

        # Calculate average latency
        for service, data in stats.items():
            data["average_latency"] = data["total_latency"] / data["count"]

        return stats

    def top_error_users(self, entries: list[dict], top_n: int = 5) -> list[tuple[str, int]]:
        """
        Retourne les utilisateurs ayant le plus d'erreurs (niveau ERROR).
        Retourne une liste de tuples (user, count) triée par count décroissant.
        """
        error_counts = {}
        for entry in entries:
            if entry["level"] == "ERROR" and entry["user"]:
                error_counts[entry["user"]] = error_counts.get(entry["user"], 0) + 1

        # Sort by count descending and return top N
        sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_errors[:top_n]