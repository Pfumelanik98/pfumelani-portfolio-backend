from django.test import TestCase

from .models import Profile
from .serializers import ProfileSerializer, SkillSerializer


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


class ProfilePhoneNumberTests(TestCase):
    def test_phone_number_is_included_in_profile_serializer(self):
        profile = Profile.objects.create(
            full_name="Pfumelani Rikhotso",
            phone_number="27604249990",
        )

        self.assertEqual(ProfileSerializer(profile).data["phone_number"], "27604249990")
