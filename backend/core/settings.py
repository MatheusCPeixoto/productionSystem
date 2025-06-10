from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-bz27=od1sq8=wz#@64_yzxq#-n3udtl0ia$^)8&7yi16j^m!^0'


DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_spectacular',
    'django_filters',
    'corsheaders',

    'activitys',
    'calendar_production',
    'enterprises',
    'equipments',
    'locations',
    'non_conformities',
    'orders',
    'production_tracking',
    'products',
    'stop_reasons',
    'structures',
    'users_erp',
    'workforces',
    'workstation'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'BASE_TESTE',
        'USER': 'sa',
        'PASSWORD': 'mcl2014',
        'HOST': '10.27.1.201',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}


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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # ...
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # ...
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API Produção',
    'DESCRIPTION': 'API do sistema Fabric',
    'VERSION': '1.0.0',
    #'SERVE_INCLUDE_SCHEMA': False, # Para servir o esquema via /api/schema/
    # Mais configurações disponíveis
}

# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:63343",
    "http://127.0.0.1:63342",
    "http://localhost:63342",
    "http://127.0.0.1:63343",
    # Adicione variações se necessário
]