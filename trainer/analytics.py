import csv
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Max, Q, Sum
from django.db.models.functions import ExtractHour, TruncDate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Attempt, Language, SiteVisit, Snippet

User = get_user_model()


def format_duration(seconds: float) -> str:
    """Format seconds into human-readable hours and minutes."""
    if not seconds or seconds <= 0:
        return '0 мин'
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 0:
        return f"{hours} ч {minutes} мин"
    return f"{minutes} мин"


def get_analytics_data(period: str = '7d') -> dict:
    """
    Computes comprehensive analytics data for the admin dashboard:
    - Daily visits and unique visitors
    - 24-hour hourly traffic pattern
    - Language popularity and typing performance
    - Device and browser breakdown
    - Popular snippets and leaderboard
    """
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)

    if period == 'today':
        start_date = today_start
        days_count = 1
    elif period == '30d':
        days_count = 30
        start_date = today_start - timedelta(days=days_count - 1)
    elif period == 'all':
        days_count = 60
        first_visit = SiteVisit.objects.order_by('timestamp').first()
        start_date = first_visit.timestamp if first_visit else (today_start - timedelta(days=29))
    else:  # default '7d'
        days_count = 7
        start_date = today_start - timedelta(days=days_count - 1)

    # Base querysets filtered by period
    visits_qs = SiteVisit.objects.filter(timestamp__gte=start_date)
    attempts_qs = Attempt.objects.filter(created_at__gte=start_date)

    # 1. Summary KPIs
    today_visits_qs = SiteVisit.objects.filter(timestamp__gte=today_start)
    yesterday_visits_qs = SiteVisit.objects.filter(
        timestamp__gte=yesterday_start, timestamp__lt=today_start
    )

    today_views = today_visits_qs.count()
    yesterday_views = yesterday_visits_qs.count()

    today_unique = (
        today_visits_qs.values('session_key')
        .exclude(session_key='')
        .distinct()
        .count()
        or today_visits_qs.values('ip_address').distinct().count()
    )
    yesterday_unique = (
        yesterday_visits_qs.values('session_key')
        .exclude(session_key='')
        .distinct()
        .count()
        or yesterday_visits_qs.values('ip_address').distinct().count()
    )

    total_period_views = visits_qs.count()
    total_period_unique = (
        visits_qs.values('session_key')
        .exclude(session_key='')
        .distinct()
        .count()
        or visits_qs.values('ip_address').distinct().count()
    )

    total_attempts_period = attempts_qs.count()
    total_attempts_all = Attempt.objects.count()

    avg_wpm_period = attempts_qs.aggregate(Avg('wpm'))['wpm__avg'] or 0.0
    avg_acc_period = attempts_qs.aggregate(Avg('accuracy'))['accuracy__avg'] or 0.0

    total_practice_seconds = attempts_qs.aggregate(Sum('time_seconds'))['time_seconds__sum'] or 0.0

    total_registered_users = User.objects.count()
    today_active_users = today_visits_qs.filter(user__isnull=False).values('user').distinct().count()
    new_signups_period = User.objects.filter(date_joined__gte=start_date).count()

    # 2. Daily Timeline (Сколько пользователей заходит в сутки)
    daily_stats = []
    daily_labels = []
    daily_unique_data = []
    daily_views_data = []
    daily_attempts_data = []

    # Build chronological dates list
    curr = start_date.date()
    end_curr = now.date()
    while curr <= end_curr:
        day_start = timezone.make_aware(timezone.datetime.combine(curr, timezone.datetime.min.time()))
        day_end = day_start + timedelta(days=1)

        d_visits = SiteVisit.objects.filter(timestamp__gte=day_start, timestamp__lt=day_end)
        d_attempts = Attempt.objects.filter(created_at__gte=day_start, created_at__lt=day_end)
        d_signups = User.objects.filter(date_joined__gte=day_start, date_joined__lt=day_end).count()

        views_cnt = d_visits.count()
        unique_cnt = (
            d_visits.values('session_key').exclude(session_key='').distinct().count()
            or d_visits.values('ip_address').distinct().count()
        )
        active_users_cnt = d_visits.filter(user__isnull=False).values('user').distinct().count()
        attempts_cnt = d_attempts.count()

        date_str = curr.strftime('%d.%m')
        weekday_ru = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'][curr.weekday()]
        label = f"{weekday_ru}, {date_str}"

        daily_labels.append(label)
        daily_unique_data.append(unique_cnt)
        daily_views_data.append(views_cnt)
        daily_attempts_data.append(attempts_cnt)

        daily_stats.append({
            'date': curr.strftime('%Y-%m-%d'),
            'label': label,
            'unique_visitors': unique_cnt,
            'pageviews': views_cnt,
            'active_users': active_users_cnt,
            'attempts': attempts_cnt,
            'signups': d_signups,
        })
        curr += timedelta(days=1)

    # 3. Hourly Breakdown (Почасовой график захода на сайт 00:00 - 23:00)
    hourly_views = [0] * 24
    hourly_unique = [0] * 24
    hourly_labels = [f"{h:02d}:00" for h in range(24)]

    # Compute hourly traffic for the selected period
    hourly_records = (
        visits_qs.annotate(hour=ExtractHour('timestamp', tzinfo=timezone.get_current_timezone()))
        .values('hour')
        .annotate(
            views=Count('id'),
            unique=Count('session_key', distinct=True)
        )
    )
    for rec in hourly_records:
        h = rec['hour']
        if h is not None and 0 <= h < 24:
            hourly_views[h] = rec['views']
            hourly_unique[h] = rec['unique']

    peak_hour = 0
    max_hour_views = 0
    for h, v in enumerate(hourly_views):
        if v > max_hour_views:
            max_hour_views = v
            peak_hour = h

    peak_hour_str = f"{peak_hour:02d}:00 – {peak_hour+1:02d}:00" if max_hour_views > 0 else "Нет заходов"

    # 4. Language Popularity (Популярность языков)
    languages = Language.objects.all()
    lang_stats = []
    lang_labels = []
    lang_attempts_count = []
    lang_avg_wpms = []

    for lang in languages:
        l_attempts = Attempt.objects.filter(snippet__language=lang)
        if period != 'all':
            l_attempts_period = l_attempts.filter(created_at__gte=start_date)
        else:
            l_attempts_period = l_attempts

        cnt = l_attempts_period.count()
        avg_wpm = l_attempts_period.aggregate(Avg('wpm'))['wpm__avg'] or 0.0
        avg_acc = l_attempts_period.aggregate(Avg('accuracy'))['accuracy__avg'] or 0.0
        total_sec = l_attempts_period.aggregate(Sum('time_seconds'))['time_seconds__sum'] or 0.0
        snippet_count = Snippet.objects.filter(language=lang).count()

        lang_stats.append({
            'name': lang.name,
            'slug': lang.slug,
            'icon': lang.icon,
            'attempts_count': cnt,
            'all_time_attempts': l_attempts.count(),
            'avg_wpm': round(avg_wpm, 1),
            'avg_accuracy': round(avg_acc, 1),
            'total_time_formatted': format_duration(total_sec),
            'snippets_count': snippet_count,
        })

    # Sort by attempts descending
    lang_stats.sort(key=lambda x: x['attempts_count'], reverse=True)
    total_lang_attempts = sum(x['attempts_count'] for x in lang_stats) or 1
    for item in lang_stats:
        item['share_pct'] = round((item['attempts_count'] / total_lang_attempts) * 100, 1)
        lang_labels.append(item['name'])
        lang_attempts_count.append(item['attempts_count'])
        lang_avg_wpms.append(item['avg_wpm'])

    # 5. Difficulty Distribution
    diff_stats = []
    diff_labels = ['Easy', 'Medium', 'Hard']
    diff_counts = []
    for diff_slug, diff_name in [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]:
        d_attempts = attempts_qs.filter(snippet__difficulty=diff_slug)
        cnt = d_attempts.count()
        avg_wpm = d_attempts.aggregate(Avg('wpm'))['wpm__avg'] or 0.0
        diff_counts.append(cnt)
        diff_stats.append({
            'slug': diff_slug,
            'name': diff_name,
            'count': cnt,
            'avg_wpm': round(avg_wpm, 1),
            'share_pct': round((cnt / (total_attempts_period or 1)) * 100, 1),
        })

    # 6. Audience & Devices
    device_qs = visits_qs.values('device_type').annotate(cnt=Count('id')).order_by('-cnt')
    device_labels = []
    device_counts = []
    for d in device_qs:
        dtype = d['device_type']
        name_map = {'desktop': 'ПК / Десктоп', 'mobile': 'Смартфоны', 'tablet': 'Планшеты', 'bot': 'Боты'}
        device_labels.append(name_map.get(dtype, dtype.capitalize()))
        device_counts.append(d['cnt'])

    browser_qs = (
        visits_qs.exclude(browser='')
        .values('browser')
        .annotate(cnt=Count('id'))
        .order_by('-cnt')[:6]
    )
    browser_stats = [{'browser': b['browser'], 'count': b['cnt']} for b in browser_qs]

    # 7. Top Visited Pages
    top_paths_qs = (
        visits_qs.values('path')
        .annotate(views=Count('id'), unique=Count('session_key', distinct=True))
        .order_by('-views')[:10]
    )
    top_paths = [
        {
            'path': p['path'],
            'views': p['views'],
            'unique': p['unique'],
            'share_pct': round((p['views'] / (total_period_views or 1)) * 100, 1),
        }
        for p in top_paths_qs
    ]

    # 8. Top Snippets
    top_snippets_qs = (
        attempts_qs.values(
            'snippet__id', 'snippet__title', 'snippet__language__name', 'snippet__difficulty'
        )
        .annotate(
            attempts_cnt=Count('id'),
            avg_wpm=Avg('wpm'),
            avg_acc=Avg('accuracy')
        )
        .order_by('-attempts_cnt')[:8]
    )
    top_snippets = [
        {
            'id': s['snippet__id'],
            'title': s['snippet__title'],
            'language': s['snippet__language__name'],
            'difficulty': s['snippet__difficulty'],
            'attempts': s['attempts_cnt'],
            'avg_wpm': round(s['avg_wpm'] or 0, 1),
            'avg_acc': round(s['avg_acc'] or 0, 1),
        }
        for s in top_snippets_qs
    ]

    # 9. Leaderboard Users
    top_users_qs = (
        User.objects.filter(attempts__isnull=False)
        .annotate(
            total_attempts=Count('attempts', distinct=True),
            total_seconds=Sum('attempts__time_seconds'),
            avg_wpm=Avg('attempts__wpm'),
            max_wpm=Max('attempts__wpm'),
        )
        .order_by('-total_attempts')[:10]
    )
    top_users = [
        {
            'username': u.username,
            'is_staff': u.is_staff,
            'attempts': u.total_attempts,
            'practice_time': format_duration(u.total_seconds),
            'avg_wpm': round(u.avg_wpm or 0, 1),
            'max_wpm': round(u.max_wpm or 0, 1),
            'joined': u.date_joined.strftime('%d.%m.%Y'),
        }
        for u in top_users_qs
    ]

    # 10. Recent Activity Log (12 items)
    recent_visits = SiteVisit.objects.select_related('user').order_by('-timestamp')[:12]
    recent_activity = []
    for v in recent_visits:
        user_display = v.user.username if v.user else 'Гость'
        recent_activity.append({
            'time': v.timestamp.strftime('%H:%M:%S'),
            'date': v.timestamp.strftime('%d.%m'),
            'type': 'visit',
            'user': user_display,
            'is_auth': bool(v.user),
            'path': v.path,
            'device': v.device_type,
            'browser': v.browser or 'Unknown',
            'ip': v.ip_address or '—',
        })

    return {
        'period': period,
        'days_count': days_count,
        'kpis': {
            'today_views': today_views,
            'yesterday_views': yesterday_views,
            'today_unique': today_unique,
            'yesterday_unique': yesterday_unique,
            'total_period_views': total_period_views,
            'total_period_unique': total_period_unique,
            'total_attempts_period': total_attempts_period,
            'total_attempts_all': total_attempts_all,
            'avg_wpm_period': round(avg_wpm_period, 1),
            'avg_acc_period': round(avg_acc_period, 1),
            'total_practice_formatted': format_duration(total_practice_seconds),
            'total_registered_users': total_registered_users,
            'today_active_users': today_active_users,
            'new_signups_period': new_signups_period,
            'peak_hour_str': peak_hour_str,
            'peak_hour_views': max_hour_views,
        },
        'daily': {
            'labels': daily_labels,
            'unique': daily_unique_data,
            'views': daily_views_data,
            'attempts': daily_attempts_data,
            'table': list(reversed(daily_stats)),
        },
        'hourly': {
            'labels': hourly_labels,
            'views': hourly_views,
            'unique': hourly_unique,
            'peak_hour': peak_hour,
            'peak_views': max_hour_views,
        },
        'languages': {
            'labels': lang_labels,
            'attempts': lang_attempts_count,
            'avg_wpms': lang_avg_wpms,
            'table': lang_stats,
        },
        'difficulties': {
            'labels': diff_labels,
            'counts': diff_counts,
            'table': diff_stats,
        },
        'devices': {
            'labels': device_labels,
            'counts': device_counts,
        },
        'browsers': browser_stats,
        'top_paths': top_paths,
        'top_snippets': top_snippets,
        'top_users': top_users,
        'recent_activity': recent_activity,
    }


@staff_member_required(login_url='admin:login')
def admin_analytics_view(request):
    """Render the full admin analytics dashboard template."""
    period = request.GET.get('period', '7d')
    if period not in ('today', '7d', '30d', 'all'):
        period = '7d'

    data = get_analytics_data(period=period)
    return render(request, 'admin/analytics.html', {'analytics': data})


@staff_member_required(login_url='admin:login')
def admin_analytics_api(request):
    """JSON API endpoint for dashboard dynamic period switching and auto-refresh."""
    period = request.GET.get('period', '7d')
    if period not in ('today', '7d', '30d', 'all'):
        period = '7d'

    data = get_analytics_data(period=period)
    return JsonResponse(data)


@staff_member_required(login_url='admin:login')
def admin_export_csv(request, export_type: str):
    """Export analytics data to CSV format for reporting."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="sprintcoder_{export_type}_{timezone.now():%Y%m%d}.csv"'
    # BOM for Excel utf-8 compatibility
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)

    if export_type == 'languages':
        writer.writerow(['Язык', 'Slug', 'Всего попыток (всё время)', 'Ср. скорость (WPM)', 'Ср. точность (%)', 'Сниппетов в базе'])
        langs = Language.objects.all()
        for lang in langs:
            attempts = Attempt.objects.filter(snippet__language=lang)
            cnt = attempts.count()
            avg_wpm = round(attempts.aggregate(Avg('wpm'))['wpm__avg'] or 0.0, 1)
            avg_acc = round(attempts.aggregate(Avg('accuracy'))['accuracy__avg'] or 0.0, 1)
            snips = Snippet.objects.filter(language=lang).count()
            writer.writerow([lang.name, lang.slug, cnt, avg_wpm, avg_acc, snips])

    elif export_type == 'visits':
        writer.writerow(['Дата и время (UTC)', 'Путь', 'Пользователь', 'Устройство', 'Браузер', 'IP-адрес', 'Статус'])
        visits = SiteVisit.objects.select_related('user').order_by('-timestamp')[:5000]
        for v in visits:
            u_name = v.user.username if v.user else 'Гость'
            writer.writerow([
                v.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                v.path,
                u_name,
                v.device_type,
                v.browser,
                v.ip_address or '',
                v.status_code
            ])
    else:
        # Default daily summary
        data = get_analytics_data('30d')
        writer.writerow(['Дата', 'Уникальные посетители', 'Просмотры страниц', 'Активные пользователи', 'Тренировок выполнено', 'Новых регистраций'])
        for row in data['daily']['table']:
            writer.writerow([
                row['date'],
                row['unique_visitors'],
                row['pageviews'],
                row['active_users'],
                row['attempts'],
                row['signups'],
            ])

    return response
