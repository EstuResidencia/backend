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
        "canon_cop",
        "area_m2",
        "piso",
        "comuna",
        "estado_cambiado",
    )

admin.site.register(Publicacion, PublicacionAdmin)
