from django.conf import settings


def debug_context(request):
    """
    Returns debug state to template
    :param request:
    :return: DEBUG status in bool
    """
    return {'debug': bool(settings.DEBUG)}
