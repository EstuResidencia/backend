from django.contrib import admin
from arriendos.models import Imagen


class ImagenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "publicacion",
        "data",
        "fecha",
    )

admin.site.register(Imagen, ImagenAdmin)