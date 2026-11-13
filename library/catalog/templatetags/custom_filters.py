from django import template

register = template.Library()

@register.filter
def format_currency(value):
    """Форматировать цену в рублях."""
    return f"{value} ₽"