from django.urls import path, include

app_name = "teknopark"

urlpatterns = [
    path("api/", include("teknopark.api.urls", namespace="teknopark_api")),
]
