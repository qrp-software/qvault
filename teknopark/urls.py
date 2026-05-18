from django.urls import include, path

from teknopark import views

app_name = "teknopark"

urlpatterns = [
    path("api/", include("teknopark.api.urls", namespace="teknopark_api")),
    path("admin/users/", views.TeknoparkUserListView.as_view(), name="admin_user_list"),
    path(
        "admin/users/<int:teknopark_user_id>/",
        views.TeknoparkUserDetailView.as_view(),
        name="admin_user_detail",
    ),
    path(
        "admin/users/<int:teknopark_user_id>/logs/",
        views.TeknoparkPDKSEntryLogListView.as_view(),
        name="admin_user_log_list",
    ),
    path("admin/daily/", views.TeknoparkPDKSEntryListView.as_view(), name="admin_entry_list"),
    path(
        "admin/monthly-reports/",
        views.TeknoparkPDKSMonthlyReportListView.as_view(),
        name="admin_monthly_report_list",
    ),
]
