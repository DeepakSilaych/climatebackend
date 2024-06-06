from .models import Blog
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'date_posted', 'author', 'image']

class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'date_posted', 'author', 'image']