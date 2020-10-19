from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# 등록하면 admin 페이지에 form을 자동으로 생성해준다

# user을 admin에 등록한다. 아래 class로 통제해서
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ user admin class """

    fieldsets = UserAdmin.fieldsets + (
        (
            "custom profile",
            {
                "fields": (
                    "avatar", "gender", "bio",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )
# admin.site.register(models.User, CustomUserAdmin) 와 동일

