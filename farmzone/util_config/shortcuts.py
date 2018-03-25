from django import shortcuts
from django.http import Http404
from .custom_exceptions import CustomAPI404Exception


def get_object_or_404(klass, *args, **kwargs):
    """
    Uses Django's get_object_or_404 to get an object
    On receiving Http404 error, a customAPI404Exception is raised
    which will be handled by the Custom Exception handler
    """
    on_error = kwargs.pop('on_error')
    try:
        object = shortcuts.get_object_or_404(klass, *args, **kwargs)
    except Http404 as e:
        response = on_error
        raise CustomAPI404Exception(response)
    return object


def get_list_or_404(klass, *args, **kwargs):
    """
    Uses Django's get_list_or_404 to get a list of objects
    On receiving Http404 error, a customAPI404Exception is raised
    which will be handled by the Custom Exception handler
    """
    on_error = kwargs.pop('on_error')
    try:
        object = shortcuts.get_list_or_404(klass, *args, **kwargs)
    except Http404 as e:
        response = on_error
        raise CustomAPI404Exception(response)
    return object
