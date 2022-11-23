from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class PatientsAdmin(admin.ModelAdmin):
    list_display = ('admin', 'gender')
    search_fields = ["admin__username"]


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Stock)
admin.site.register(Category)
