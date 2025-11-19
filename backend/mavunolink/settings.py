import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql

# Setup MySQL
pymysql.install_as_MySQLdb()

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------
# 🔐 Django Core Settings
# ---------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

AUTH_USER_MODEL = 'accounts.User'


# ✅ Allow localhost and your ngrok domain (update this when ngrok changes)
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "e50ea3b90fe9.ngrok-free.app",  # ← your current ngrok domain
]

# ---------------------------------------------------------
# 📦 Installed Apps
# ---------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your custom apps
    'accounts',
    'products',
    'marketplace',
    'verification',
    'chatbot',
    'reviews',
    'orders',
]

# ---------------------------------------------------------
# ⚙️ Middleware
# ---------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mavunolink.urls'

# ---------------------------------------------------------
# 🧩 Templates
# ---------------------------------------------------------
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

WSGI_APPLICATION = 'mavunolink.wsgi.application'

# ---------------------------------------------------------
# 🗄️ Database (MySQL)
# ---------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mavuno',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ---------------------------------------------------------
# 💳 M-Pesa Configuration
# ---------------------------------------------------------
MPESA_ENV = os.getenv("MPESA_ENV", "sandbox")
MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY", "")
MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "")
MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE", "174379")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY", "")

# ✅ Your live callback URL (from ngrok)
MPESA_CALLBACK_URL = "https://e50ea3b90fe9.ngrok-free.app/api/mpesa/callback/"

# ---------------------------------------------------------
# 🌍 Localization
# ---------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ---------------------------------------------------------
# 🖼️ Static & Media
# ---------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
