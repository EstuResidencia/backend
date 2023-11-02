from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    ROLES_CHOICES = [
        ("A", "ARRENDADOR"),
        ("E", "ESTUDIANTE"),
    ]
    usuario_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
        editable=False,
    )
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50, unique=True)
    tipo_documento = models.CharField(max_length=2, blank=True, null=True)
    documento = models.IntegerField(unique=True, blank=True, null=True)
    password = models.CharField(db_column="contrasena")
    celular = models.CharField()
    foto = models.BinaryField(blank=True, null=True)
    rol = models.CharField(max_length=1, choices=ROLES_CHOICES, blank=True, null=True)
    validado = models.BooleanField(default=False)

    # Remove username field and use email as unique identifier
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre", "celular"] # Maybe faltan

    # Use custom user manager
    objects = UserManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(tipo_documento__in=["CC", "CE", "TI", "PP"]),
                name="valid_tipo_documento",
            ),
            models.CheckConstraint(
                check=models.Q(rol__in=["A", "E"]),
                name="valid_rol",
            )
        ]

    def __str__(self) -> str:
        return self.nombre