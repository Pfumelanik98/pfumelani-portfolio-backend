from django.db import models

class Profile(models.Model):
    full_name = models.CharField(max_length=150)
    professional_title = models.CharField(max_length=150, blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=32, blank=True)
    location = models.CharField(max_length=150, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): return self.full_name
    class Meta:
        verbose_name = "Portfolio profile"
        verbose_name_plural = "Portfolio profile"

class Skill(models.Model):
    class Proficiency(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        DEVELOPING = "developing", "Developing"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20, choices=Proficiency.choices, default=Proficiency.DEVELOPING)
    description = models.TextField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    def __str__(self): return self.name
    class Meta: ordering = ["display_order", "name"]
