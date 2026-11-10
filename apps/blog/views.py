from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import BlogPost, BlogCategory
from .serializers import BlogPostSerializer, BlogCategorySerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    def get_queryset(self):
        qs = BlogPost.objects.select_related("category")
        return qs if self.request.user.is_authenticated else qs.filter(status=BlogPost.Status.PUBLISHED)

class BlogCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = BlogCategory.objects.all()
