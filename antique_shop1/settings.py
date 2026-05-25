from pathlib import Path
from decouple import config, Csv
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ── БЕЗОПАСНОСТЬ ──────────────────────────────────────
# ── БЕЗОПАСНОСТЬ ──────────────────────────────────────
SECRET_KEY = config('SECRET_KEY', default='django-insecure-local-dev-key-change-in-production')
DEBUG      = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost,web-production-40c55.up.railway.app,*.up.railway.app', cast=Csv())
# ── ДОБАВЬТЕ ЭТИ СТРОКИ ────────────────────────────────
# CSRF и CORS настройки для Railway
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-40c55.up.railway.app',
    'https://*.up.railway.app',  # все поддомены Railway
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Для работы с прокси (Railway использует reverse proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Куки для HTTPS (важно для Railway)
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← для статики
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'antique_shop1.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'antique_shop1.wsgi.application'

# ── БАЗА ДАННЫХ ───────────────────────────────────────
DATABASE_URL = config('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

# ── ПАРОЛИ ────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── ЯЗЫК И ВРЕМЯ ─────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Nicosia'
USE_I18N = True
USE_TZ   = True

# ── СТАТИКА И МЕДИА ───────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'