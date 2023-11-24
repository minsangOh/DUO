"""
Django settings for final_pjt_back project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y&g@!ahcujj^o(5mnxd0&l^i@*m1n4ku1x3z^!sjye4@nm8e1_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'DESKTOP-MDJG1NJ']

# Application definition

INSTALLED_APPS = [
    # APP
    'accounts',
    'articles',
    'apis',

    # DRF
    'rest_framework',
    'rest_framework.authtoken',

    # REST_AUTH
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # django-cors-headers
    'corsheaders',

    # django-extensions
    'django_extensions',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # django-cors-headers 추가에 따른 MIDDLEWARE 추가
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

# 브라우저 정책에 따른 허용하는 출처 주소
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
]

SITE_ID = 1

# DRF auth settings
REST_FRAMEWORK = {
    # Authentication
    # Token 인증을 기본으로 사용하도록 설정
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # permission
    # API 접근에 대한 기본 권한 설정. 모든 요청 허용
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


ROOT_URLCONF = 'final_pjt_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 템플릿 디렉토리 설정
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

WSGI_APPLICATION = 'final_pjt_back.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 사용자 수정
AUTH_USER_MODEL = 'accounts.User'

# ALL AUTH 수정
# dj-rest-auth 는 email 을 필수적으로 사용하도록 기본 설정 ==> 따라서 해당 사항을 선택사항(False)으로 수정
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = None

# django 인증 시스템에서 사용할 백엔드 클래스 지정
# 기본 인증 백엔드와 allauth 패키지에서 제공하는 인증 백엔드를 모두 사용하겠다는 설정.
AUTHENTICATION_BACKENDS = (
    # django 기본 인증 백엔드
    "django.contrib.auth.backends.ModelBackend",
    # django-allauth 패키지에서 제공하는 인증 백엔드 클래스.
    "allauth.account.auth_backends.AuthenticationBackend",
)

# rest-auth가 회원 가입 시 accounts 앱에서 구현한 serializer 호출하도록 설정
REST_AUTH = {
    'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
}

import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

os.environ.get('EXIM_KEY') # 기본 사용방법