from django.contrib import admin
from arriendos.models import Publicacion


class PublicacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "inquilino",
        "descripcion",
        "estado",
        "direccion",
        "tipo_residencia",
        "canon_cop",
        "area_m2",
        "habitaciones",
        "piso",
        "comuna",
        "estado_cambiado",
    )

admin.site.register(Publicacion, PublicacionAdmin)
