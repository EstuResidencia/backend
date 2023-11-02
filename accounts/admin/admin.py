from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ..models.user import User
# Register your models here.


class CustomUserAdmin(UserAdmin):
    """
    Class to customize the user administration panel
    """

    model = User
    list_display = (
        "usuario_id",
        "nombre",
        "correo",
        "tipo_documento",
        "documento",
        "celular",
        "rol",
        "foto",
        "validado",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "validado",
        "nombre",
        "documento"
    )
    fieldsets = (
        ("Information", {"fields": ("nombre",
                                    "correo",
                                    "tipo_documento",
                                    "documento",
                                    "password",
                                    "celular",
                                    "rol",
                                    "foto",
                                    "validado")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "correo",
                    "nombre",
                    "tipo_documento",
                    "documento",
                    "password1",
                    "password2",
                    "celular",
                    "rol",
                    "foto",
                    "validado",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email", "nombre", "documento", "validado")
    ordering = ("usuario_id",)


admin.site.register(User, CustomUserAdmin)
