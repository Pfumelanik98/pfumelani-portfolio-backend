from django.contrib import admin
from .models import Project, ProjectTechnology

class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "is_published", "created_at")
    list_filter = ("status", "is_published")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectTechnologyInline]
