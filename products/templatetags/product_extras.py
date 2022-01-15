from django import template

# Definiciones para funciones para filtros
register = template.Library()

@register.filter()
def price_format(value):
    return '${0:.2f}'.format(value)
