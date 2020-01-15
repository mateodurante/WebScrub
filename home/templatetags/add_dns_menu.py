import re
from django.utils.safestring import mark_safe
from django import template
register = template.Library()


re_url = re.compile(r'[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')

def add_tags(url):
    return '<div class="dropdown inline-menu">  <span id="dLabel" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+url.group()+'<span class="caret"></span>  </span>  <ul class="dropdown-menu" aria-labelledby="dLabel"> <li><a href="/dns?url='+url.group()+'">Más información del nombre de dominio</a></li>  </ul> </div>'

@register.filter
def add_dns_menu(value):
    string = str(value)
    return mark_safe(re_url.sub(add_tags,string))
