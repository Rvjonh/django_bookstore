import random
from django import template

register = template.Library()


@register.simple_tag
def random_rgba_color(alpha=1):
    red_color = random.randint(0, 255)
    green_color = random.randint(0, 255)
    blue_color = random.randint(0, 255)
    if alpha is None:
        return f"rgba({red_color}, {green_color}, {blue_color},1)"
    return f"rgba({red_color}, {green_color}, {blue_color}, {alpha})"
