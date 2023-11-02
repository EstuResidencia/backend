from django.db import models

from arriendos.models.publicacion import Publicacion


class Resena(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    usuario = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="resenas",
    )
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name="resenas",
    )
    comentario = models.CharField(null=True, blank=True)
    calificacion = models.IntegerField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(calificacion__gte=1) & models.Q(calificacion__lte=10),
                name="valid_calificacion",
            ),
        ]
