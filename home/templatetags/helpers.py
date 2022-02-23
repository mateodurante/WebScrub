from django import template
import json
import math

register = template.Library()

@register.filter
def order_by_order(queryset):
   return queryset.order_by("order") 

@register.filter
def get_item(collection, key):
    if type(collection) == dict:
        return collection.get(key, '')
    elif type(collection) in [list, tuple]:
        return collection[key]
    return ''

@register.filter
def get_items_from_dict_list(collection, key):
    return [getattr(c, key) for c in collection]

@register.filter
def as_list(value):
    return list(value)

@register.filter
def json_loads(value):
    try:
        return json.loads(value)
    except:
        return value

@register.filter
def convert_size(size_bytes):
    try:
        size_bytes = int(size_bytes)
    except:
        return size_bytes
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    # s = int(round(size_bytes / p, 0))
    return f"{s} {size_name[i]}"

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

@register.filter
def slugger(value):
    return value.replace(' ', '-')
