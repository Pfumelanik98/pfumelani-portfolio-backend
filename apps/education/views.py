from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Education, Certificate, Resume
from .serializers import EducationSerializer, CertificateSerializer, ResumeSerializer

class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Education.objects.all()

class CertificateViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        qs = Certificate.objects.all()
        return qs if self.request.user.is_authenticated else qs.filter(is_published=True)

class ResumeView(generics.RetrieveAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self):
        return Resume.objects.filter(is_active=True).first()
