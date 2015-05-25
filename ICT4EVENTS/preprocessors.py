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

    context['google_api_key'] = "AIzaSyC2E9WBTy_FhPgl35Qes98lQUxkvm78vmM"

    return context