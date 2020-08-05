"""
WSGI config for majorproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

# env = environ.Env()
# env.read_env()

ENVIRONMENT_TYPE = "production"

if ENVIRONMENT_TYPE == 'development':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'majorproject.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'majorproject.settings.production')


application = get_wsgi_application()
application = DjangoWhiteNoise(application)
