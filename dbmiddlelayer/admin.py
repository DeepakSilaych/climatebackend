from django.contrib import admin
from .models import AWSDataForquater

class AWSDataForquaterAdmin(admin.ModelAdmin):
    list_display = ('station', 'rainfall', 'timestamp')
    search_fields = ('station', 'rainfall', 'timestamp')
    list_filter = ('station', 'rainfall', 'timestamp')
    ordering = ('-timestamp', 'station')


admin.site.register(AWSDataForquater, AWSDataForquaterAdmin)