from events.models import Event


def base(request):
    """
    Adds basic context to each request.
    :param request:
    :return:
    """
    context = {}
    if request.user.is_active:
        context['pre_events'] = Event.objects.all()

    return context