import datetime
from django.utils import timezone


DAY_NAMES_EN = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
DAY_NAMES_RU = {0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 4: 'Пт', 5: 'Сб', 6: 'Вс'}


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


def get_user_streak(user) -> dict:
    """
    Calculate the daily exercise streak for a user.
    A user achieves a streak by completing at least one exercise (Attempt) per calendar day.

    Returns a dict with:
      - current_streak: int (active consecutive days)
      - best_streak: int (all-time longest consecutive days)
      - practiced_today: bool (whether user has completed an exercise today)
      - practiced_yesterday: bool (whether user completed an exercise yesterday)
      - streak_active: bool (current_streak > 0)
      - status: str ('completed_today', 'pending_today', 'broken', 'new', 'guest')
      - status_text: str (human-readable status in English)
      - status_text_ru: str (human-readable status in Russian)
      - total_active_days: int (total unique days practiced)
      - recent_week: list[dict] (last 7 days chronologically up to today)
      - recent_14_days: list[dict] (last 14 days chronologically up to today)
    """
    today = timezone.localdate()
    yesterday = today - datetime.timedelta(days=1)

    def _build_days_list(num_days: int, dates_set: set) -> list:
        days = []
        for i in range(num_days - 1, -1, -1):
            d = today - datetime.timedelta(days=i)
            days.append({
                'date': d,
                'date_str': d.isoformat(),
                'day_name': DAY_NAMES_EN.get(d.weekday(), d.strftime('%a')),
                'day_name_ru': DAY_NAMES_RU.get(d.weekday(), ''),
                'day_number': d.day,
                'is_today': (i == 0),
                'completed': (d in dates_set),
            })
        return days

    if user is None or not getattr(user, 'is_authenticated', False):
        return {
            'current_streak': 0,
            'best_streak': 0,
            'practiced_today': False,
            'practiced_yesterday': False,
            'streak_active': False,
            'status': 'guest',
            'status_text': 'Sign in to track your daily streak!',
            'status_text_ru': 'Войдите, чтобы отслеживать стрик!',
            'total_active_days': 0,
            'recent_week': _build_days_list(7, set()),
            'recent_14_days': _build_days_list(14, set()),
        }

    # Fetch all distinct dates on which this user completed at least 1 attempt
    distinct_dates = set(
        user.attempts
        .values_list('created_at__date', flat=True)
    )

    practiced_today = today in distinct_dates
    practiced_yesterday = yesterday in distinct_dates

    # 1. Calculate current streak
    current_streak = 0
    if practiced_today:
        current_streak = 1
        d = yesterday
        while d in distinct_dates:
            current_streak += 1
            d -= datetime.timedelta(days=1)
    elif practiced_yesterday:
        current_streak = 1
        d = yesterday - datetime.timedelta(days=1)
        while d in distinct_dates:
            current_streak += 1
            d -= datetime.timedelta(days=1)

    # 2. Calculate all-time best streak
    sorted_dates = sorted(distinct_dates)
    best_streak = 0
    run = 0
    prev = None
    for d in sorted_dates:
        if prev is not None and d == prev + datetime.timedelta(days=1):
            run += 1
        else:
            run = 1
        if run > best_streak:
            best_streak = run
        prev = d

    best_streak = max(best_streak, current_streak)
    total_active_days = len(distinct_dates)

    # 3. Status and messages
    if practiced_today:
        status = 'completed_today'
        if current_streak == 1:
            status_text = "Streak started! Completed today 🔥"
            status_text_ru = "Стрик начат! Завершено сегодня 🔥"
        else:
            status_text = f"{current_streak}-day streak! Completed today 🔥"
            status_text_ru = f"Стрик {current_streak} дн.! Завершено сегодня 🔥"
    elif current_streak > 0:
        status = 'pending_today'
        status_text = f"{current_streak}-day streak! Practice today to keep it alive ⏳"
        status_text_ru = f"Стрик {current_streak} дн.! Пройди тренировку сегодня ⏳"
    elif total_active_days > 0:
        status = 'broken'
        status_text = "Streak lost. Complete an exercise today to restart!"
        status_text_ru = "Стрик прерван. Пройди упражнение сегодня, чтобы начать заново!"
    else:
        status = 'new'
        status_text = "Complete an exercise today to start your streak!"
        status_text_ru = "Пройди упражнение сегодня, чтобы начать стрик!"

    return {
        'current_streak': current_streak,
        'best_streak': best_streak,
        'practiced_today': practiced_today,
        'practiced_yesterday': practiced_yesterday,
        'streak_active': (current_streak > 0),
        'status': status,
        'status_text': status_text,
        'status_text_ru': status_text_ru,
        'total_active_days': total_active_days,
        'recent_week': _build_days_list(7, distinct_dates),
        'recent_14_days': _build_days_list(14, distinct_dates),
    }
