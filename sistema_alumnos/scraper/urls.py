from django.urls import path
from .views import buscar_wikipedia

app_name = "scraper"
urlpatterns = [
    path("", buscar_wikipedia, name="buscar"),
]
