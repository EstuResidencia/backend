from django.urls import path
from .views import (
    notificacion_views,
    publicacion_views,
    resena_views,
    solicitud_views,
)

notificacion_urls = [
    path("notification-signal/", notificacion_views.notification_signal, name="notification_signal"),
]

publicacion_urls = [
    path("publicacion/",
         publicacion_views.create_read_publicacion,
         name="create_read_publicacion"),
    path("publicacion/<int:publicacion_id>/",
         publicacion_views.update_delete_get_publicacion,
         name="update_delete_publicacion"),
    path("publicacion/listar/<int:arrendador_id>/",
         publicacion_views.read_publicacion_by_arrendador,
         name="read_publicacion_by_arrendador"),
]

resena_urls = [
    path("resena/<publicacion_id>/", resena_views.create_read_resena, name="create_read_resena"),
]

solicitud_urls = [
    path("solicitud/",
         solicitud_views.create_solicitud,
         name="create_solicitud"),
    path("solicitud/<int:solicitud_id>/",
         solicitud_views.read_update_delete_solicitud,
         name="read_update_delete_solicitud"),
    path("solicitud/estudiante/<int:estudiante_id>/",
         solicitud_views.read_solicitud_by_estudiante,
         name="read_solicitud_by_estudiante"),
    path("solicitud/arrendador/<int:arrendador_id>/",
         solicitud_views.read_solicitud_by_arrendador,
         name="read_solicitud_by_arrendador"),
]

urlpatterns = (
    notificacion_urls
    + publicacion_urls
    + resena_urls
    + solicitud_urls
)
