from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    # str도 사용가능
    list_display = ("__str__", "rating_average")

