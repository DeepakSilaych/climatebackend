from django.contrib import admin
from django.urls import path, include
from dbmiddlelayer.views import health_check
from django.contrib import admin

admin.site.site_header = 'Mumbai Flood App'                    # default: "Django Administration"
admin.site.index_title = 'Our Systems'                 # default: "Site administration"
admin.site.site_title = 'Mumbai Flood Admin Panel' # default: "Django site admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('health/', health_check),

    path('blogs/', include('blogs.urls')),
    path('cs/', include('crowdsource.urls')),
    path('aw/', include('awsstations.urls')),
    path('weather/', include('weatherstations.urls')),  
    path('db/', include('dbmiddlelayer.urls')),

]
