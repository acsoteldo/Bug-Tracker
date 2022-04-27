from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


def priority_widget(priority, size="xs", type="button"):
    priority_map = {
        "1": ["danger", "Critical"],
        "2": ["warning", "High"],
        "3": ["success", "Normal"],
        "4": ["info", "Low"],
        "5": ["secondary", "Very Low"],
    }

    attr = priority_map.get(priority)
    if type == "button":
        html = '<button type="button" class="btn btn-{0} btn-{1}">{2}</button>'
        html = html.format(attr[0], size, attr[1])
    else:
        html = '<span class="badge bg-{}">{}</span>'
        html = html.format(attr[0], attr[1])
    return html

def status_widget(status, size="xs", type="button"):

    status_map = {
        "new": ["success", "New"],
        "accepted": ["info", "Accepted"],
        "assigned": ["primary", "Assigned"],
        "re-opened": ["warning", "Re-Opened"],
        "closed": ["secondary", "Closed"],
    }

    attr = status_map.get(status.lower(), ["secondary", status])

    if size == "lg" and status in ("closed", "duplicate", "split"):
        attr[0] = "danger"

    if type == "button":
        html = '<button type="button" class="btn btn-{0} btn-{1}">{2}</button>'
        html = html.format(attr[0], size, attr[1])
    else:
        html = '<span class="badge bg-{}">{}</span>'
        html = html.format(attr[0], attr[1])

    return html

@register.filter
@stringfilter
def format_action(string):

    action_map = {
        "re-opened": "Re-Open",
        "closed": "Close",
        "new": "New",
        "accept": "Accept",
        "comment": "Comment on ",
        "assign": "Assign",
    }

    return mark_safe(action_map.get(string, string))


@register.simple_tag(takes_context=True)
def query_transform(context, include_page=False, **kwargs):

    query = context["request"].GET.copy()
    for k, v in kwargs.items():
        query[k] = v

    if query.get("page") and not include_page:
        query.pop("page")
    return query.urlencode()
