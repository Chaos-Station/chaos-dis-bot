from datetime import datetime, timezone


def get_round_duration(start_time: str) -> str:
    try:
        start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - start

        total_seconds = int(delta.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours}ч {minutes}м {seconds}с"
        else:
            return f"{minutes}м {seconds}с"

    except Exception:
        return "неизвестно"
