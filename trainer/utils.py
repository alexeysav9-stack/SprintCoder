def format_exercise_time(seconds: float) -> dict:
    """
    Format exercise duration in seconds into Steam-like hours and minutes.

    Returns a dictionary with:
      - total_seconds: int
      - hours: int
      - minutes: int
      - seconds: int
      - formatted: str (e.g. "1 hr 15 mins", "57 mins", "0 mins")
      - formatted_ru: str (e.g. "1 ч. 15 мин.", "57 мин.", "0 мин.")
      - formatted_short: str (e.g. "1h 15m", "57m")
      - steam_hours: float (e.g. 1.2 hrs on record)
    """
    total = max(0, int(round(seconds)))
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60

    if hours > 0:
        hr_str = f"{hours} hr{'s' if hours != 1 else ''}"
        min_str = f"{minutes} min{'s' if minutes != 1 else ''}"
        if minutes > 0:
            formatted_en = f"{hr_str} {min_str}"
            formatted_ru = f"{hours} ч. {minutes} мин."
            formatted_short = f"{hours}h {minutes}m"
        else:
            formatted_en = hr_str
            formatted_ru = f"{hours} ч."
            formatted_short = f"{hours}h"
    elif minutes > 0:
        formatted_en = f"{minutes} min{'s' if minutes != 1 else ''}"
        formatted_ru = f"{minutes} мин."
        formatted_short = f"{minutes}m"
    else:
        if total > 0:
            formatted_en = f"{total} sec{'s' if total != 1 else ''}"
            formatted_ru = f"{total} сек."
            formatted_short = f"{total}s"
        else:
            formatted_en = "0 mins"
            formatted_ru = "0 мин."
            formatted_short = "0m"

    steam_hours = round(total / 3600, 1)

    return {
        'total_seconds': total,
        'hours': hours,
        'minutes': minutes,
        'seconds': secs,
        'formatted': formatted_en,
        'formatted_ru': formatted_ru,
        'formatted_short': formatted_short,
        'steam_hours': steam_hours,
    }
