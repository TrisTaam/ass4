from django import template

register = template.Library()

@register.filter
def get_id(item):
    return str(item._id)  # Convert _id to a string for URL compatibility