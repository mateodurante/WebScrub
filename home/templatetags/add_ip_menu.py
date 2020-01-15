import re
from django.utils.safestring import mark_safe
from django import template
register = template.Library()


re_ipv4 = re.compile(r'[0-9]+(?:\.[0-9]+){3}')

def add_tags(ip):
    return """
        <a href="/rdap?ip="""+ip.group()+"""">
            <div>
                <span id="dLabel" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    """+ip.group()+"""
                </span>
                <span class="glyphicon glyphicon-plus">  </span>
            </div>
        </a>

        """

@register.filter
def add_ip_menu(value):
    string = str(value)
    return mark_safe(re_ipv4.sub(add_tags,string))
