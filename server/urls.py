from django.contrib import admin
from django.urls import path, include
from dbmiddlelayer.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('health/', health_check),

    path('blogs/', include('blogs.urls')),
    path('cs/', include('crowdsource.urls')),
    path('aws/', include('awsstations.urls')),
    path('weather/', include('weatherstations.urls')),  
    path('db/', include('dbmiddlelayer.urls')),

]
