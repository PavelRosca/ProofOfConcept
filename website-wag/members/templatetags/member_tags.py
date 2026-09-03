from django import template

from members.access import is_active_member as _is_active_member

register = template.Library()


@register.filter
def is_active_member(user):
    return _is_active_member(user)
