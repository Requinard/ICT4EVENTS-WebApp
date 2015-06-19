from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def linkify(value):
    value = str(value)

    extension = value.split('.')[-1]
    print(value)
    if extension in ["jpg", "jpeg", "gif", "png"]:
        return "<img src='{0}' class='img-responsive'>".format(value)
    elif extension in ["mp3", "wav", "ogg"]:
        print("<audio controls><source='{0}'></audio>".format(value))
        return '<audio src="{0}" controls><a href="{0}"> Download</a></audio>'.format(value)
    elif extension in ["webm", ]:
        return '<video src="{0}" controls class="img-responsive">you browser doesnt support embedded video. <a href="{0}>Download it here</a></video>'.format(
            value)
    else:
        return '<a href="{0}" class="btn btn-warning">Download dit bestand</a>'.format(value)


@register.filter
@stringfilter
def audit(value):
    # Deze wordenlijst is bepaald door experts
    bad_words = ["fuck", "kanker", "kut", "tering", "tyfus", "klote", "Mike", "Martijn", "Oracle", "Mathijs"]

    for word in bad_words:
        if word in value:
            value = value.replace(word, "*"*len(word))

    return value
