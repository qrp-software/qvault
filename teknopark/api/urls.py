from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("logs", views.TeknoparkPDKSEntryLogViewSet, basename="pdkse-entry-log")
router.register("daily", views.TeknoparkPDKSEntryViewSet, basename="pdks-entry")
router.register(
    "monthly", views.TeknoparkPDKSMonthlyReportViewSet, basename="pdks-monthly-report"
)

app_name = "teknopark_api"

urlpatterns = [
    path("pdks/", include(router.urls)),
]

