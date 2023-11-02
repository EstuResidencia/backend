from django.db import models


class Publicacion(models.Model):
    ESTADOS_CHOICES = [
        ("P", "PENDIENTE"),
        ("A", "ACTIVA"),
        ("O", "OCUPADA"),
        ("R", "RECHAZADA"),
    ]

    TIPO_RESIDENCIA_CHOICES = [
        ("A", "APARTAMENTO"),
        ("C", "CASA"),
        ("H", "HABITACION"),
    ]

    COMUNA_CHOICES = [
        ("1", "POPULAR"),
        ("2", "SANTA CRUZ"),
        ("3", "MANRIQUE"),
        ("4", "ARANJUEZ"),
        ("5", "CASTILLA"),
        ("6", "DOCE DE OCTUBRE"),
        ("7", "ROBLEDO"),
        ("8", "VILLA HERMOSA"),
        ("9", "BUENOS AIRES"),
        ("10", "LA CANDELARIA"),
        ("11", "LAURELES ESTADIO"),
        ("12", "LA AMERICA"),
        ("13", "SAN JAVIER"),
        ("14", "EL POBLADO"),
        ("15", "GUAYABAL"),
        ("16", "BELEN"),
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
        related_name="publicaciones"
    )
    inquilino = models.OneToOneField(
        "accounts.User",
        related_name="residencia",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    descripcion = models.CharField()
    estado = models.CharField(
        max_length=1,
        choices=ESTADOS_CHOICES,
        default="P"
    )
    direccion = models.CharField(max_length=100)
    tipo_residencia = models.CharField(
        max_length=1,
        choices=TIPO_RESIDENCIA_CHOICES
    )
    canon_cop = models.IntegerField()
    area_m2 = models.IntegerField()
    habitaciones = models.IntegerField(default=1)
    piso = models.IntegerField(default=1)
    comuna = models.CharField(max_length=2, choices=COMUNA_CHOICES)
    estado_cambiado = models.BooleanField(default=True)


    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(estado__in=["P", "A", "O", "R"])),
                name="valid_estado_publicacion",
            ),
            models.CheckConstraint(
                check=(models.Q(tipo_residencia__in=["A", "C", "H"])),
                name="valid_tipo_residencia",
            )
        ]
