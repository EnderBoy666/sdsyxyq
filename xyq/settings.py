"""
Django settings for xyq project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^!qp3^zapydu^-2z*p_@z3j%awpqxo01evys3c#btmsh&=m*-@'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('DEBUG') == 'TRUE':
    DEBUG=True
else:
    DEBUG=False
# 当DEBUG设置为False时Django报错，通常是由于以下几个常见原因：
# 1. ALLOWED_HOSTS设置不正确：Django要求在生产环境中明确指定允许访问的主机。
# 2. 静态文件配置问题：在生产环境中，需要正确配置静态文件的处理。
# 3. CSRF_TRUSTED_ORIGINS设置：如果应用使用了跨域请求，需要配置信任的源。

# 以下是一些可能的解决方案：

# 1. 检查ALLOWED_HOSTS设置
# 确保ALLOWED_HOSTS包含你的生产环境域名或IP地址。
# 例如：
# ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '127.0.0.1']

# 2. 静态文件配置
# 确保静态文件的收集和存储配置正确。
# 例如，在settings.py中添加以下配置：
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 3. CSRF_TRUSTED_ORIGINS设置
# 如果应用使用了跨域请求，确保CSRF_TRUSTED_ORIGINS包含你的生产环境域名。
# 例如：
# CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']

# 4. 错误日志记录
# 在settings.py中配置日志记录，以便更好地调试错误。
# 例如：
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': 'error.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }

# 请根据具体的错误信息进行排查和修复。如果问题仍然存在，请提供详细的错误信息，以便进一步诊断。

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://sdsyxyq.onrender.com',  # Render 域名
    'http://localhost:8000',         # 本地开发环境
]

# Application definition

INSTALLED_APPS = [
    #我的应用程序
    'xyq_files',
    'users',

    #第三方应用程序
    'bootstrap4',

    #默认添加的应用程序
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'xyq.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'xyq_files.context_processors.unread_count_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'xyq.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # 必须放在 AuthenticationMiddleware 之前
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 用户认证
    'django.contrib.messages.middleware.MessageMiddleware',  # 消息框架
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 如果使用 Whitenoise 处理静态文件
]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_USER_MODEL = 'users.CustomUser'
