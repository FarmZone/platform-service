from rest_framework.response import Response
from rest_framework.views import exception_handler

from .custom_exceptions import CustomAPI404Exception, CustomAPI400Exception


def custom_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    Checks if CustomAPI404Exception is raised, sends a custom response then
    Otherwise calls standard error response
    """
    if isinstance(exc, CustomAPI404Exception) or isinstance(exc,CustomAPI400Exception):
        return Response(exc.response, exc.status_code)
    else:
        return exception_handler(exc, context)
