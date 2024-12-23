import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'as8as687A$#RSWEFWR%#@@@!$%¨&&¨*¨*(*6f!9&8+=3c0rjh4mz5hl14d=!04*+djw@'

DEBUG = True

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.humanize',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'usuarios',
    'salas',
    'reservas',
    'localflavor',
]

X_FRAME_OPTIONS='SAMEORIGIN'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#ALLOWED_HOSTS = ['192.168.15.96','10.0.6.169']
ALLOWED_HOSTS = ["*"]
STATICSTORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
CSRF_TRUSTED_ORIGINS= ["https://sdo.up.railway.app"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'usuarios.Usuario'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = '/usuarios/login/'  # Substitua pela URL correta para sua página de login

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# tempo limite da sessão em segundos (1 hora)
SESSION_COOKIE_AGE = 3600

# redirecionar para a página de login quando a sessão expirar
SESSION_EXPIRE_REDIRECT_URL = '/'

# se definido como True, o tempo limite de sessão será estendido após cada atividade do usuário
SESSION_SAVE_EVERY_REQUEST = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'zanellabruno7@gmail.com'
EMAIL_HOST_PASSWORD = 'wron fcmr ugbj ufhb'
DEFAULT_FROM_EMAIL = 'zanellabruno7@gmail.com'
ADMINS = [('Admin Zanella', 'zanellabruno7@gmail.com')]
