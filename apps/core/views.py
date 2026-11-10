from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Profile, Skill
from .serializers import ProfileSerializer, SkillSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self):
        return get_object_or_404(Profile.objects.order_by("-updated_at"))

class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        qs = Skill.objects.all()
        return qs if self.request.user.is_authenticated else qs.filter(is_published=True)
