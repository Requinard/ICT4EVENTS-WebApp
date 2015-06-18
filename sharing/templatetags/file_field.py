from django import template

register = template.Library()

def linkify(value):
    value = str(value)

    extension = value.split('.')[-1]

    if extension in ["jpg", "jpeg", "gif", "png"]:
        return "<img src='{}' class='img-responsive'" % value