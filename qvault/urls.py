from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from qvault import views
from . import views
from keychain import views as keychain_views
from django.views.generic import RedirectView

ADMIN_URL = 'admin/'

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("robots.txt", views.RobotsView.as_view()),
    path("welcome/", views.WelcomePage.as_view(), name="welcome"),
    path("thanks/", views.ThanksPage.as_view(), name="thanks"),
    path('', RedirectView.as_view(url='/keychain/', permanent=False), name='home'),
    path("keychain/", include("keychain.urls", namespace="keychain")),
    path("teknopark/", include("teknopark.urls", namespace="teknopark")),
    path("users/api/", include("users.api.urls", namespace="users_api")),
]

urlpatterns += i18n_patterns(
    path("", views.HomePage.as_view(), name="home"),
    path("users/", include("users.urls", namespace="users")),
)

# Static and media files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

