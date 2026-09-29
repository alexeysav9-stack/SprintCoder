import re
from django.utils import timezone


IGNORE_PREFIXES = (
    '/static/',
    '/media/',
    '/favicon.ico',
    '/robots.txt',
    '/admin/',
    '/api/',
    '/healthz',
    '/ping',
)

ASSET_REGEX = re.compile(r'\.(css|js|map|png|jpe?g|gif|ico|svg|woff2?|ttf|eot)$', re.IGNORECASE)


class VisitTrackingMiddleware:
    """
    Lightweight middleware to track user page visits for admin traffic analytics.
    Records unique sessions, IP addresses, paths, devices, and browsers without blocking requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.record_visit(request, response)
        return response

    def record_visit(self, request, response):
        try:
            # Only track GET requests to actual content pages
            if request.method != 'GET':
                return

            path = request.path

            # Skip ignored paths (static assets, admin panel, internal api calls)
            for prefix in IGNORE_PREFIXES:
                if path.startswith(prefix) or path == prefix:
                    return

            if ASSET_REGEX.search(path):
                return

            # Ensure session is created if possible to track unique visitors
            session_key = ''
            if hasattr(request, 'session'):
                if not request.session.session_key:
                    request.session.save()
                session_key = request.session.session_key or ''

            # Extract user if authenticated
            user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None

            # Extract IP address (supports reverse proxies like Nginx/Cloudflare)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            ua = request.META.get('HTTP_USER_AGENT', '')
            device_type = self.detect_device(ua)

            # Never record automated bots, crawlers, or uptime monitoring pings in visitor analytics
            if device_type == 'bot':
                return

            referer = request.META.get('HTTP_REFERER', '')[:500]
            browser = self.detect_browser(ua)

            status_code = getattr(response, 'status_code', 200)

            # Lazy import to avoid any circular dependency at startup
            from .models import SiteVisit
            SiteVisit.objects.create(
                path=path[:255],
                ip_address=ip if ip and len(ip) <= 45 else None,
                user=user,
                session_key=session_key[:64],
                user_agent=ua[:500],
                device_type=device_type,
                browser=browser[:50],
                referer=referer,
                status_code=status_code,
            )
        except Exception:
            # Analytics recording must never break or slow down user requests
            pass

    @staticmethod
    def detect_device(ua: str) -> str:
        ua_lower = ua.lower()
        if any(b in ua_lower for b in (
            'bot', 'crawl', 'spider', 'slurp', 'mediapartners', 'lighthouse',
            'uptimerobot', 'pingdom', 'cron-job', 'betteruptime', 'healthcheck',
            'monitor', 'kuma', 'curl', 'wget', 'python-requests', 'urllib',
        )):
            return 'bot'
        if any(t in ua_lower for t in ('ipad', 'tablet', 'kindle', 'playbook')):
            return 'tablet'
        if any(m in ua_lower for m in ('mobile', 'android', 'iphone', 'ipod', 'blackberry', 'windows phone')):
            return 'mobile'
        return 'desktop'

    @staticmethod
    def detect_browser(ua: str) -> str:
        ua_lower = ua.lower()
        if 'edg/' in ua_lower or 'edge/' in ua_lower:
            return 'Edge'
        if 'yabrowser' in ua_lower:
            return 'Yandex'
        if 'opr/' in ua_lower or 'opera' in ua_lower:
            return 'Opera'
        if 'firefox' in ua_lower:
            return 'Firefox'
        if 'chrome' in ua_lower:
            return 'Chrome'
        if 'safari' in ua_lower:
            return 'Safari'
        return 'Other'
