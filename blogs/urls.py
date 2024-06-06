# urls

from django.urls import path
from .views import BlogList, BlogDetail


urlpatterns = [
    path('', BlogList.as_view()),
    path('<int:blog_id>/', BlogDetail.as_view())
]