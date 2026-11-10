from django.test import TestCase

from .serializers import ProjectSerializer


class ProjectPublicationTests(TestCase):
    def test_project_can_be_published_through_serializer(self):
        serializer = ProjectSerializer(data={
            "title": "Portfolio API",
            "slug": "portfolio-api",
            "description": "A portfolio backend.",
            "is_published": True,
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)
        project = serializer.save()

        self.assertTrue(project.is_published)
