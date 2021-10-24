from django import template

register = template.Library()


@register.filter(name='to_int')
def to_int(value):
    return int(value)

@register.filter(name='round_num')
def round_num(value):
    return round(value,2)



@register.filter(name='int_temp')
def int_temp(value):
    return int(value)+30



