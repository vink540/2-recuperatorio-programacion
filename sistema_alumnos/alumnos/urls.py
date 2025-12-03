from django.urls import path
from . import views

app_name = "alumnos"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("crear/", views.crear_alumno, name="crear_alumno"),
    path("generar_pdf/<int:pk>/", views.generar_pdf_enviar, name="generar_pdf"),
    path('editar/<int:pk>/', views.editar_alumno, name='editar_alumno'),
    path('eliminar/<int:pk>/', views.eliminar_alumno, name='eliminar_alumno'),
    path("export_csv/", views.export_csv, name="export_csv"),
    
]
