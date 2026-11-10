from rest_framework import serializers
from apps.core.models import Skill
from apps.core.serializers import SkillSerializer
from .models import Project, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["id", "image", "alt_text", "caption", "display_order"]
        read_only_fields = ["id"]

class ProjectSerializer(serializers.ModelSerializer):
    technologies = SkillSerializer(many=True, read_only=True)
    technology_ids = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, write_only=True, source="technologies", required=False)
    images = ProjectImageSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ["id", "title", "slug", "short_description", "description", "problem_statement", "solution", "role", "technologies", "technology_ids", "github_url", "live_url", "status", "featured", "is_published", "display_order", "images", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
    def create(self, validated_data):
        technologies = validated_data.pop("technologies", [])
        project = super().create(validated_data)
        project.technologies.set(technologies)
        return project
    def update(self, instance, validated_data):
        technologies = validated_data.pop("technologies", None)
        project = super().update(instance, validated_data)
        if technologies is not None: project.technologies.set(technologies)
        return project
