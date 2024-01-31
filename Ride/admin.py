from django.contrib import admin

from Ride.models import Ride


class RideAdmin(admin.ModelAdmin):
    list_display = ('owner', 'driver', 'dst_addr', 'status', 'time_created')
    list_display_links = ('owner', 'driver', 'dst_addr')
    readonly_fields = ('dst_addr', 'status', 'time_created')
    ordering = ('-time_created',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(Ride, RideAdmin)