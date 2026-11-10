from rest_framework import serializers
from .models import BlogPost, BlogCategory

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ["id", "name", "slug"]
        read_only_fields = ["id"]

class BlogPostSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=BlogCategory.objects.all(), source="category", write_only=True, required=False, allow_null=True)
    class Meta:
        model = BlogPost
        fields = ["id", "category", "category_id", "title", "slug", "content", "excerpt", "featured_image", "status", "published_at", "created_at", "updated_at"]
        read_only_fields = ["id", "published_at", "created_at", "updated_at"]
