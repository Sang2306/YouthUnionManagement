from django import template
# Su dung custom filter
register = template.Library()


@register.filter(name='asia_hcm_time')
def asia_hcm_time(time):
    """
        Custom template de lay user time hien thi tren bang cac hoat dong
    """
    return str(time)[11:16]
