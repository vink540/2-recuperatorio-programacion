from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("alumnos/", include("alumnos.urls", namespace="alumnos")),
    path("scraper/", include("scraper.urls", namespace="scraper")),
    path("", RedirectView.as_view(pattern_name="alumnos:dashboard", permanent=False)),
]
