from django.db import models
from arriendos.models.publicacion import Publicacion


class Solicitud(models.Model):
    ESTADOS_CHOICES = [
        (1, "PENDIENTE"),
        (2, "APROBADA"),
        (3, "CANCELADA"),
        (4, "RECHAZADA"),
    ]

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
        related_name="solicitudes"
    )
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="solicitudes"
    )
    estado = models.IntegerField(choices=ESTADOS_CHOICES, default=1)
    pagado = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True)
    estado_cambiado = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(estado__in=[1, 2, 3, 4]),
                name="valid_estado_solicitud",
            ),
        ]


