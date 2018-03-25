"""
WSGI config for farmzone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
from __future__ import unicode_literals, absolute_import
import newrelic.agent
import os

#newrelic.agent.initialize('newrelic.ini', os.environ.get('CURRENT_ENV', 'development'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farmzone.settings.production")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
