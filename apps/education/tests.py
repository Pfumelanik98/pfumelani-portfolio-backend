from django.test import TestCase

from .serializers import CertificateSerializer


class CertificatePublicationTests(TestCase):
    def test_certificate_can_be_published_through_serializer(self):
        serializer = CertificateSerializer(data={
            "title": "Django Certificate",
            "issuer": "Training Provider",
            "is_published": True,
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)
        certificate = serializer.save()

        self.assertTrue(certificate.is_published)
