from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from .models import ContactMessage
from .serializers import ContactMessageCreateSerializer

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageCreateSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
