from django.contrib import admin
from .models import Profile, Skill

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "professional_title", "updated_at")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "is_published")
    list_filter = ("category", "proficiency", "is_published")
    search_fields = ("name",)
