from django import template
from django.utils.safestring import mark_safe
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

@register.simple_tag()
def whatsapp_link(telephone):
    telephone = telephone.strip()
    if telephone != "":
        return mark_safe("<a href='https://wa.me/+34%s'><i class='zmdi zmdi-whatsapp'></i></a>"%telephone.strip('+34'))
    else:
        return ""