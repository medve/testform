"""
WSGI config for testform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testform.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
