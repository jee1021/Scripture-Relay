import environ
from pathlib import Path

# ────────────────────────────────────────────────
# 프로젝트 기본 경로 설정
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# 환경변수 초기화
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')   # .env 파일 읽기 (없으면 무시됨)

# ────────────────────────────────────────────────
# 기본 Django 설정
# ────────────────────────────────────────────────
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# ────────────────────────────────────────────────
# Application definition
# ────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.ninja',
    'app.scripture_relay',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ────────────────────────────────────────────────
# Database
# ────────────────────────────────────────────────
DATABASES = {
    'default': env.db(               # django-environ이 자동으로 파싱해줌
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3')
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = env('LANGUAGE_CODE', default='ko-kr')
TIME_ZONE = env('TIME_ZONE', default='Asia/Seoul')
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = env('STATIC_ROOT', default=BASE_DIR / 'staticfiles')
MEDIA_URL = 'media/'
MEDIA_ROOT = env('MEDIA_ROOT', default=BASE_DIR / 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

