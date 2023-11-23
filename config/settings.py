from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured

from datetime import timedelta


# Base Directory 경로
BASE_DIR = Path(__file__).resolve().parent.parent

# secrets.json 경로
SECRETS_PATH = os.path.join(BASE_DIR, "secrets.json")

# secrets.json 파일
secret_file = os.path.join(BASE_DIR, "secrets.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())


# 환경변수 가져오기
def get_env(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_env("SECRET_KEY")

# Debug 모드 설정
DEBUG = True

# Host 설정
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # library
    "rest_framework",
    'corsheaders',
    'storages',
    # apps
    "table",
    "accounts",
    "home",
    "post",
    "mypage",
    "apply",
    "evaluation",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # 전역 설정!!
        # 따라서 view에서 별도로 @authentication_classes([TokenAuthentication]) 안 해줘도 됨!!!
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "ROTATE_REFRESH_TOKENS": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True # <- 모든 호스트 허용 (배포 전에 우선 이렇게 ㄱㄱ)


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# aws RDS연결하기 위한 설정 변경
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # engine: mysql
        'NAME' : get_env("NAME"),  # DB Name
        'USER' : get_env("USER"),  # DB User
        'PASSWORD' : get_env("PASSWORD"),  # Password
        'HOST': get_env("HOST"), # 생성한 데이터베이스 엔드포인트
        'PORT': 3306, # 데이터베이스 포트
        'OPTIONS':{
            'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "table.User"  # User 재정의 setting 추가



# S3 관련 세팅
AWS_ACCESS_KEY_ID = get_env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'sogangcrews'
AWS_S3_REGION_NAME = 'ap-northeast-2' 
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# AWS_DEFAULT_ACL = 'public-read'
# AWS_QUERYSTRING_AUTH = False

# Static Setting
# STATIC_LOCATION = 'static'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media Setting
MEDIA_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
