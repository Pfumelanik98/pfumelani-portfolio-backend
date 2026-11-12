from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
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
        self.assertFalse(serializer.save().is_published)


class ProfilePhoneNumberTests(TestCase):
    def test_phone_number_is_included_in_profile_serializer(self):
        profile = Profile.objects.create(
            full_name="Pfumelani Rikhotso",
            phone_number="27604249990",
        )
        self.assertEqual(ProfileSerializer(profile).data["phone_number"], "27604249990")


class BootstrapSuperuserTests(TestCase):
    def setUp(self):
        self.password = "Q7!m" + ("z" * 20)
        self.environment = {
            "DJANGO_BOOTSTRAP_SUPERUSER": "true",
            "DJANGO_BOOTSTRAP_SUPERUSER_USERNAME": "production-admin",
            "DJANGO_BOOTSTRAP_SUPERUSER_EMAIL": "admin@example.com",
            "DJANGO_BOOTSTRAP_SUPERUSER_PASSWORD": self.password,
        }

    def test_bootstrap_is_a_no_op_without_environment_configuration(self):
        output = StringIO()
        with patch.dict("os.environ", {}, clear=True):
            call_command("bootstrap_superuser", stdout=output)
        self.assertIn("not requested", output.getvalue())
        self.assertFalse(get_user_model().objects.exists())

    def test_bootstrap_rejects_partial_environment_configuration(self):
        with patch.dict("os.environ", {"DJANGO_BOOTSTRAP_SUPERUSER": "true"}, clear=True):
            with self.assertRaisesMessage(CommandError, "Incomplete"):
                call_command("bootstrap_superuser")

    def test_bootstrap_creates_superuser_without_printing_password(self):
        output = StringIO()
        with patch.dict("os.environ", self.environment, clear=True):
            call_command("bootstrap_superuser", stdout=output)
        user = get_user_model().objects.get(username="production-admin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(self.password))
        self.assertNotIn(self.password, output.getvalue())

    def test_existing_user_is_not_changed_without_explicit_opt_in(self):
        user_model = get_user_model()
        original_password = "R8!n" + ("y" * 20)
        user_model.objects.create_superuser(
            username="production-admin",
            email="admin@example.com",
            password=original_password,
        )
        with patch.dict("os.environ", self.environment, clear=True):
            with self.assertRaisesMessage(CommandError, "already exists"):
                call_command("bootstrap_superuser")
        user = user_model.objects.get(username="production-admin")
        self.assertTrue(user.check_password(original_password))
        self.assertFalse(user.check_password(self.password))

    def test_existing_superuser_password_can_be_reset_with_explicit_opt_in(self):
        user_model = get_user_model()
        original_password = "R8!n" + ("y" * 20)
        user_model.objects.create_superuser(
            username="production-admin",
            email="admin@example.com",
            password=original_password,
        )
        environment = {
            **self.environment,
            "DJANGO_BOOTSTRAP_SUPERUSER_RESET_EXISTING": "true",
        }
        output = StringIO()
        with patch.dict("os.environ", environment, clear=True):
            call_command("bootstrap_superuser", stdout=output)
        user = user_model.objects.get(username="production-admin")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.check_password(original_password))
        self.assertNotIn(self.password, output.getvalue())

    def test_existing_regular_user_cannot_be_promoted_or_changed(self):
        user_model = get_user_model()
        original_password = "R8!n" + ("y" * 20)
        user_model.objects.create_user(
            username="production-admin",
            email="admin@example.com",
            password=original_password,
        )
        environment = {
            **self.environment,
            "DJANGO_BOOTSTRAP_SUPERUSER_RESET_EXISTING": "true",
        }
        with patch.dict("os.environ", environment, clear=True):
            with self.assertRaisesMessage(CommandError, "not a superuser"):
                call_command("bootstrap_superuser")
        user = user_model.objects.get(username="production-admin")
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(original_password))
        self.assertFalse(user.check_password(self.password))
