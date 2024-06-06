from rest_framework.views import APIView
from .models import Blog
from .serializers import BlogSerializer, BlogListSerializer
from rest_framework.response import Response


class BlogList(APIView):
    def get(self, request):
        blog = Blog.objects.all()
        serializer = BlogListSerializer(blog, many=True)
        return Response(serializer.data)

class BlogDetail(APIView):
    def get(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)