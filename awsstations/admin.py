from django.contrib import admin
from .models import AWSStation, DaywisePrediction, TrainStation, StationData, HourlyPrediction



class AWSStationAdmin(admin.ModelAdmin):
    list_display = ('station_id', 'name', 'latitude', 'longitude', 'rainfall')
    search_fields = ('name', 'station_id')
    list_filter = ('rainfall', 'latitude', 'longitude')
    ordering = ('station_id', 'name', 'rainfall')
    list_display_links = ('station_id', 'name')
    list_filter = ('station_id', 'name', 'latitude', 'longitude', 'rainfall')
    fieldsets = (
        ('AWS Station', {
            'fields': ('station_id', 'name', 'latitude', 'longitude', 'rainfall')
        }),
    )

class DaywisePredictionAdmin(admin.ModelAdmin):
    list_display = ('station', 'timestamp', 'day1_rainfall', 'day2_rainfall', 'day3_rainfall')
    search_fields = ('station', 'timestamp')
    list_filter = ('station', 'timestamp', 'day1_rainfall', 'day2_rainfall', 'day3_rainfall')
    ordering = ('station', 'timestamp', 'day1_rainfall', 'day2_rainfall', 'day3_rainfall')
    list_editable = ('day1_rainfall', 'day2_rainfall', 'day3_rainfall', 'timestamp')
    list_filter = ('station', 'timestamp', 'day1_rainfall', 'day2_rainfall', 'day3_rainfall')
    fieldsets = (
        ('Daywise Prediction', {
            'fields': ('station', 'timestamp', 'day1_rainfall', 'day2_rainfall', 'day3_rainfall')
        }),
    )

class TrainStationAdmin(admin.ModelAdmin):
    list_display = ('station_code', 'station_name', 'latitude', 'longitude', 'neareststation', 'WarningLevel')
    search_fields = ('station_code', 'station_name', 'neareststation', 'warningLevel' )
    list_filter = ('station_code', 'station_name', 'latitude', 'longitude', 'neareststation', 'WarningLevel')
    ordering = ('station_code', 'station_name', 'latitude', 'longitude', 'neareststation', 'WarningLevel')
    list_editable = ('neareststation', 'WarningLevel')
    list_filter = ('station_code', 'station_name', 'neareststation', 'WarningLevel')
    fieldsets = (
        ('Train Station', {
            'fields': ('station_code', 'station_name', 'latitude', 'longitude', 'neareststation', 'WarningLevel')
        }),
    )

class StationDataAdmin(admin.ModelAdmin):
    list_display = ('station', 'rainfall', 'timestamp')
    search_fields = ('station', 'timestamp')
    list_filter = ('station', 'rainfall', 'timestamp')
    ordering = ('station', 'rainfall', 'timestamp')
    list_editable = ['rainfall']
    list_filter = ('station', 'rainfall', 'timestamp')
    fieldsets = (
        ('Station Data', {
            'fields': ('station', 'rainfall', 'timestamp')
        }),
    )

class HourlyPredictionAdmin(admin.ModelAdmin):
    list_display = ('station', 'timestamp', 'hr_24_rainfall')
    search_fields = ('station', 'timestamp')
    list_filter = ('station', 'timestamp', 'hr_24_rainfall')
    ordering = ('station', 'timestamp', 'hr_24_rainfall')
    list_editable = ['hr_24_rainfall']
    list_filter = ('station', 'timestamp', 'hr_24_rainfall')
    fieldsets = (
        ('Hourly Prediction', {
            'fields': ('station', 'timestamp', 'hr_24_rainfall')
        }),
    )



admin.site.register(AWSStation, AWSStationAdmin)
admin.site.register(DaywisePrediction, DaywisePredictionAdmin)
admin.site.register(TrainStation, TrainStationAdmin)
admin.site.register(StationData, StationDataAdmin)
admin.site.register(HourlyPrediction, HourlyPredictionAdmin)