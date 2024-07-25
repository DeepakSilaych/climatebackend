from django.contrib import admin
from .models import AWSDataForquater

class AWSDataForquaterAdmin(admin.ModelAdmin):
    list_display = ('station', 'rainfall', 'timestamp')


admin.site.register(AWSDataForquater, AWSDataForquaterAdmin)