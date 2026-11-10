from django.db import models
from apps.core.models import Skill

class Project(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    problem_statement = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    role = models.CharField(max_length=150, blank=True)
    technologies = models.ManyToManyField(Skill, through="ProjectTechnology", related_name="projects", blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.title
    class Meta: ordering = ["display_order", "-created_at"]

class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_technologies")
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT, related_name="project_technologies")
    class Meta:
        constraints = [models.UniqueConstraint(fields=["project", "skill"], name="unique_project_skill")]

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/")
    alt_text = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["display_order", "id"]
    def __str__(self): return f"Image for {self.project.title}"
