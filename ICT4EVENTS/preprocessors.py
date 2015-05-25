from events.models import Event


def base(request):
    """
    Adds basic context to each request.
    :param request:
    :return:
    """
    context = {}
    if request.user.is_active:
        try:
            context['pre_events'] = request.user.settings.GetRegistrations
        except:
            pass

    context['google_api_key'] = "AIzaSyC2E9WBTy_FhPgl35Qes98lQUxkvm78vmM"

    return context