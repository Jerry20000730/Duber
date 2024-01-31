from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Account.models import DuberUser, DuberDriver


# Register your models here.
class DuberUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin')
    list_display_links = ('username', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(DuberUser, DuberUserAdmin)
admin.site.register(DuberDriver)
