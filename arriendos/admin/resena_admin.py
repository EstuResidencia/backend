from django.contrib import admin
from arriendos.models import Resena


class ResenaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "publicacion",
        "comentario",
        "calificacion",
        "fecha",
    )

admin.site.register(Resena, ResenaAdmin)