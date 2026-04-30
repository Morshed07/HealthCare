from pathlib import Path
import environ
from datetime import timedelta
from django.urls import reverse_lazy
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)

# Read .env file
environ.Env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-morshed-nayeem-secret-key"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

CSRF_TRUSTED_ORIGINS = env(
    'CSRF_TRUSTED_ORIGINS',
).split(',')

CORS_ALLOWED_ORIGINS = env(
    'CORS_ALLOWED_ORIGINS',
).split(',')


CORS_ALLOW_HEADERS = list(default_headers) + [
    "ngrok-skip-browser-warning",
]

CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    "apps.unfold_admin",
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ======================
    # Third-party apps
    # ======================
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',

    # ======================
    # Local apps
    # ======================
    'apps.core',
    'apps.account',
    'apps.representative',
    'apps.product',
    'apps.cart',
    'apps.checkout',
    'apps.notification',
    'apps.service',
    'apps.doctor',
    'apps.consultation_type',
    'apps.appointment',


]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # whitenoise for serving static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reactides.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'reactides.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# MEDIA_ROOT
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Auth User Model
AUTH_USER_MODEL = 'account.User'

# =========================
# Whitenoise Configuration
# =========================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# ==============================
# Rest Framework Configuration
# ==============================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.JSONParser",
    ),
}


# =======================
# Email Configuration
# =======================

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)

EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default="noreply@reactides.com"
)


# =======================
# Celery Configuration
# =======================

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://127.0.0.1:6380/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://127.0.0.1:6380/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_EXPIRES = 3600  # Results expire after 1 hour
CELERY_TASK_TRACK_STARTED = True
CELERY_WORKER_POOL = "solo"
CELERY_TASK_ALWAYS_EAGER = False


# =======================
# Jwt Configuration
# =======================

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
}


# =======================
# Unfold Configuration
# =======================

UNFOLD = {
    "SITE_TITLE": "Reactides Admin",
    "SITE_HEADER": "Reactides",
    "SITE_SUBHEADER": "Admin Dashboard",
    # "SITE_LOGO": {
    #     "light": lambda request: static("admin/react.svg"),  # Path to your file
    #     "dark": lambda request: static("admin/react.svg"),   # Use same or different for dark mode
    # },
    # "SITE_SYMBOL": "speed",
    # Update this path to include the 'apps' prefix
    "DASHBOARD_CALLBACK": "apps.unfold_admin.dashboard.dashboard_callback",
    
    # Also update any other callbacks or links (Environment, Sidebar, etc.)
    "ENVIRONMENT": "apps.unfold_admin.dashboard.environment_callback",
    
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            # --- ADDED THIS DASHBOARD SECTION ---
            {
                "title": "Navigation",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard", 
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            # ------------------------------------
            {
                "title": "Account",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "group", 
                        "link": reverse_lazy("admin:account_user_changelist"),
                    },
                    {
                        "title": "Shipping Addresses",
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:account_shippingaddress_changelist"),
                    },
                ],
            },
            {
                "title": "Representative",
                "separator": True,
                "items": [
                    {
                        "title": "Representatives",
                        "icon": "badge",
                        "link": reverse_lazy("admin:representative_representative_changelist"),
                    },
                ],
            },
            {
                "title": "Product",
                "separator": True,
                "items": [
                    {
                        "title": "Products",
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:product_product_changelist"),
                    },
                ],
            },
            {
                "title": "Cart",
                "separator": True,
                "items": [
                    {
                        "title": "Carts",
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:cart_cart_changelist"),
                    },
                    {
                        "title": "Cart Items",
                        "icon": "shopping_basket",
                        "link": reverse_lazy("admin:cart_cartitem_changelist"),
                    },
                    {
                        "title": "Coupons",
                        "icon": "local_offer",
                        "link": reverse_lazy("admin:cart_coupon_changelist"),
                    },
                    {
                        "title": "Shipping Coupons",
                        "icon": "local_offer",
                        "link": reverse_lazy("admin:cart_shippingcoupon_changelist"),
                    },
                ],
            },
            {
                "title": "Checkout",
                "separator": True,
                "items": [
                    {
                        "title": "Orders",
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:checkout_order_changelist"),
                    },
                    {
                        "title": "Order Items",
                        "icon": "list_alt",
                        "link": reverse_lazy("admin:checkout_orderitem_changelist"),
                    },
                ],
            },
            {
                "title": "Notification",
                "separator": True,
                "items": [
                    {
                        "title": "Alerts",
                        "icon": "notifications",
                        "link": reverse_lazy("admin:notification_alert_changelist"),
                    },
                ],
            },
            {
                "title": "Service & Appointment",
                "separator": True,
                "items": [
                    {
                        "title": "Services",
                        "icon": "event",
                        "link": reverse_lazy("admin:service_service_changelist"),
                    },
                    {
                        "title": "Consultation Types",
                        "icon": "event",
                        "link": reverse_lazy("admin:consultation_type_consultationtype_changelist"),
                    },
                    {
                        "title": "Doctors",
                        "icon": "local_hospital",
                        "link": reverse_lazy("admin:doctor_doctor_changelist"),
                    },
                    {
                        "title": "Appointments",
                        "icon": "event",
                        "link": reverse_lazy("admin:appointment_appointment_changelist"),
                    },
                ],
            },
        ],
    },
    "COLORS": {
        "primary": {
            "50": "240 251 249",
            "100": "209 244 237",
            "200": "163 232 220",
            "300": "110 213 197",
            "400": "63 186 168",
            "500": "34 158 142",
            "600": "8 120 112",  
            "700": "12 96 90",
            "800": "13 77 73",
            "900": "14 64 61",
            "950": "4 38 36",
        },
    },
    #     "primary": {
    #             "50": "238 242 255",
    #             "100": "224 231 255",
    #             "200": "199 210 254",
    #             "300": "165 180 252",
    #             "400": "129 140 248",
    #             "500": "99 102 241",
    #             "600": "79 70 229",  # Base Indigo
    #             "700": "67 56 202",
    #             "800": "55 48 163",
    #             "900": "49 46 129",
    #             "950": "30 27 75",
    #         },
    # },
    #     "primary": {
    #             "50": "245 243 255",
    #             "100": "237 233 254",
    #             "200": "221 214 254",
    #             "300": "196 181 253",
    #             "400": "167 139 250",
    #             "500": "139 92 246",  # Base Violet
    #             "600": "124 58 237",
    #             "700": "109 40 217",
    #             "800": "91 33 182",
    #             "900": "76 29 149",
    #             "950": "46 16 101",
    #         },
    # }
        # "primary": {
        #         "50": "255 247 237",
        #         "100": "255 237 213",
        #         "200": "254 215 170",
        #         "300": "253 186 116",
        #         "400": "251 146 60",
        #         "500": "249 115 22",   # Base Orange
        #         "600": "234 88 12",
        #         "700": "194 65 12",
        #         "800": "154 52 18",
        #         "900": "124 45 18",
        #         "950": "67 20 7",
        #     },
        # },
}