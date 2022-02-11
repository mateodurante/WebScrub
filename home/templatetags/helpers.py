from django import template

register = template.Library()

@register.filter
def order_by_order(queryset):
   return queryset.order_by("order") 

@register.filter
def get_item(dictionary, key):
    if type(dictionary) == dict:
        return dictionary.get(key, '')
    return ''

@register.filter
def member(obj, name):
    return getattr(obj, name, None)

@register.filter
def mul(obj, other):
    return obj * other

@register.filter
def get_atributo(obj, name):
    return getattr(obj, name, None)

@register.filter
def get_c(obj):
    return obj.__class__.__name__
