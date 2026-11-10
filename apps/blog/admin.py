from django.contrib import admin
from .models import BlogCategory, BlogPost

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "published_at")
    list_filter = ("status", "category")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
