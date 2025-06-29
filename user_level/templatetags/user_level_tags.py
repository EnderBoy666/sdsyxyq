from django import template

register = template.Library()

@register.filter
def get_max_points(level):
    if level == 1:
        return 100
    elif level == 2:
        return 200
    elif level == 3:
        return 500
    elif level == 4:
        return 1000
    else:
        return float('inf')