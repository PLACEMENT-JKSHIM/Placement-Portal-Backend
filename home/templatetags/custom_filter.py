def has_description(list1):
    print(list1)
    for dict1 in list1:
        if dict1.mem_description:
            return True

    return False
from django import template


def to_br(value):
    return value.replace("\n","%0D%0A")

register = template.Library()

register.filter('has_description', has_description)
register.filter('to_br', to_br)