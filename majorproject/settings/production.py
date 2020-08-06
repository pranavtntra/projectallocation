from .base import *
import os, dj_database_url

DEBUG = True
SECRET_KEY = '*zfn6t@3r2yz(h@ufo%!y4al@f&-nq4x7(s2@tu*ywhib2u02_'
# DEBUG = os.environ.get('DEBUG', default=False, cast=bool)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
