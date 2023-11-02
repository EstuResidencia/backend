from django.db import models

from arriendos.models.publicacion import Publicacion


class Imagen(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name="imagenes",
    )
    data = models.BinaryField()
    fecha = models.DateField(auto_now_add=True)