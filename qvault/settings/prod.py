from .main import *

STATIC_ROOT = f"/var/cache/{DJANGO_PROJECT_NAME}/static/"
STATIC_URL = "/static/"

MEDIA_ROOT = f"/var/opt/{DJANGO_PROJECT_NAME}/media/"
MEDIA_URL = "/media/"

SITE_BASE_URL = "http://qvault.qrp.com.tr"

ALLOWED_HOSTS = [
    "qvault.qrp.com.tr",
    "www.qvault.qrp.com.tr",
]

if DEBUG:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
    AUTH_PASSWORD_VALIDATORS = []
    SECURE_SSL_REDIRECT = False
    X_FRAME_OPTIONS = env("X_FRAME_OPTIONS", default="SAMEORIGIN")

if env.bool("APPLY_EXTRA_SECURITY_SETTINGS", default=not DEBUG):
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 86400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
