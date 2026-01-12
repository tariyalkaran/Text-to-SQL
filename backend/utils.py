# utils.py
def safe_score_of(result):
    try:
        if isinstance(result, dict):
            return float(result.get("@search.score") or result.get("score") or 0.0)
        return float(getattr(result, "score", 0.0))
    except Exception:
        return 0.0
def normalize_scores(score_map):
    if not score_map:
        return {}
    max_score = max(score_map.values())
    if max_score <= 0:
        return {k: 0.0 for k in score_map}
    return {k: (v / max_score) for k, v in score_map.items()}