from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    def get_queryset(self):
        qs = Project.objects.prefetch_related("technologies", "images")
        return qs if self.request.user.is_authenticated else qs.filter(is_published=True)
