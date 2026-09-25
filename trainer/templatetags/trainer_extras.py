import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def jsonify(value):
    """Serialize a Python value to a JSON string, marked safe for inline <script> use."""
    # json.dumps handles all string escaping; mark_safe prevents Django from
    # HTML-escaping quotes (") into &quot; which would break JSON.parse().
    return mark_safe(json.dumps(value))
