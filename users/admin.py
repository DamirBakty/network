from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = models.User
    list_display = ["email", "username",]

admin.site.register(models.User, CustomUserAdmin)
