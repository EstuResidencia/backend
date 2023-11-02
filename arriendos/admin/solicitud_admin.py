from django.contrib import admin
from arriendos.models import Solicitud

class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "publicacion",
        "estado",
        "pagado",
        "fecha",
        "estado_cambiado",
    )

admin.site.register(Solicitud, SolicitudAdmin)