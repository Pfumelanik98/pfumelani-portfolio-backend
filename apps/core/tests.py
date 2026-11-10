from django.test import TestCase

from .serializers import SkillSerializer


class SkillPublicationTests(TestCase):
    def test_skill_publication_can_be_changed_through_serializer(self):
        serializer = SkillSerializer(data={
            "name": "Django",
            "category": "Backend",
            "is_published": False,
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)
        skill = serializer.save()

        self.assertFalse(skill.is_published)
