from django.contrib import admin

from .models import MapPoint


@admin.register(MapPoint)
class MapPointAdmin(admin.ModelAdmin):
    list_display = ['address', 'coordinates_update_date']
