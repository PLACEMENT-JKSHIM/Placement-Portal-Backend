def has_description(list1):
    print(list1)
    for dict1 in list1:
        if dict1.mem_description:
            return True

    return False
from django import template

register = template.Library()

register.filter('has_description', has_description)