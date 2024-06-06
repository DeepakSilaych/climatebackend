from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include('blogs.urls')),
    path('cs/', include('crowdsource.urls')),
    path('aws/', include('awsstations.urls')),
    path('weather/', include('weatherstations.urls')),
]
