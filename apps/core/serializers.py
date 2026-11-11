from rest_framework import serializers
from .models import Profile, Skill

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "full_name", "professional_title", "biography", "email", "phone_number", "location", "linkedin_url", "github_url", "profile_image", "updated_at"]
        read_only_fields = ["id", "updated_at"]

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category", "proficiency", "description", "display_order", "is_published"]
        read_only_fields = ["id"]
