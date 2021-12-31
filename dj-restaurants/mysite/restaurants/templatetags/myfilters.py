# p. 260

from django import template

def yes_no(bool_value, show_str):
    if bool_value:
        return show_str.partition('/')[0]
    else:
        return show_str.partition('/')[2]

# register this filter
register = template.Library()
register.filter('yes_no', yes_no)