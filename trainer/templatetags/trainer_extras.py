import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Mapping from Language.slug → devicons CSS class
DEVICON_CLASSES = {
    'python':     'devicon-python-plain colored',
    'javascript': 'devicon-javascript-plain colored',
    'java':       'devicon-java-plain colored',
    'cpp':        'devicon-cplusplus-plain colored',
    'go':         'devicon-go-plain colored',
    'sql':        'devicon-postgresql-plain colored',
    'css':        'devicon-css3-plain colored',
    'bash':       'devicon-bash-plain colored',
    'html':       'devicon-html5-plain colored',
    'php':        'devicon-php-plain colored',
    'csharp':     'devicon-csharp-plain colored',
}


@register.filter(is_safe=True)
def devicon_class(slug):
    """Return the devicons CSS class for a given language slug."""
    return DEVICON_CLASSES.get(slug, 'devicon-devicon-plain')


@register.simple_tag
def devicon(slug, extra_class=''):
    """Render a <i> devicons element for a language slug (or dice for 'random')."""
    if slug == 'random':
        cls = f'dice-icon {extra_class}'.strip()
        return mark_safe(f'<span class="{cls}">🎲</span>')
    cls = DEVICON_CLASSES.get(slug, 'devicon-devicon-plain')
    if extra_class:
        cls = f'{cls} {extra_class}'
    return mark_safe(f'<i class="{cls}"></i>')


@register.filter(is_safe=True)
def jsonify(value):
    """Serialize a Python value to a JSON string, marked safe for inline <script> use."""
    # json.dumps handles all string escaping; mark_safe prevents Django from
    # HTML-escaping quotes (") into &quot; which would break JSON.parse().
    return mark_safe(json.dumps(value))


@register.filter
def format_steam_time(seconds):
    """Format seconds into Steam-like hours and minutes string."""
    from ..utils import format_exercise_time
    try:
        sec = float(seconds or 0)
    except (ValueError, TypeError):
        sec = 0.0
    return format_exercise_time(sec)['formatted']


