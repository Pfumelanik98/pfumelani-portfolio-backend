from django.test import TestCase

from .serializers import CertificateSerializer


class CertificatePublicationTests(TestCase):
    def test_certificate_can_be_published_through_serializer(self):
        serializer = CertificateSerializer(data={
            "title": "Django Certificate",
            "issuer": "Training Provider",
            "issue_date": "2026-08-01",
            "expiration_date": "2036-09-01",
            "credential_id": "ABC-123",
            "skills": ["Python"],
            "is_published": True,
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)
        certificate = serializer.save()

        self.assertTrue(certificate.is_published)
        self.assertEqual(certificate.expiration_date.isoformat(), "2036-09-01")
        self.assertEqual(certificate.credential_id, "ABC-123")
        self.assertEqual(certificate.skills, ["Python"])
