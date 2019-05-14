from django import template
# Su dung custom filter
register = template.Library()


@register.filter(name='asia_hcm_time')
def asia_hcm_time(time):
    """
        Custom template de lay user time hien thi tren bang cac hoat dong
    """
    print('*'*40)
    date = str(time).split()[0]
    time = str(time).split()[1]
    date_splitted = date.split('-')
    time_splitted = time.split(':')
    return time_splitted[0] + ':' + time_splitted[1] + \
        ' ' + date_splitted[2] + '-' + date_splitted[1] + '-' + date_splitted[0]
