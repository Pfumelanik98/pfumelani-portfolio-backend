from django.db import models

class Education(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
    institution = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=150, blank=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.COMPLETED)
    description = models.TextField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["display_order", "-start_year"]
    def __str__(self): return f"{self.qualification} — {self.institution}"

class Certificate(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)
    document = models.FileField(upload_to="certificates/", blank=True)
    is_published = models.BooleanField(default=False)
    def __str__(self): return self.title

class Resume(models.Model):
    title = models.CharField(max_length=150, default="Professional CV")
    file = models.FileField(upload_to="resumes/")
    version = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_active:
            Resume.objects.exclude(pk=self.pk).update(is_active=False)
    def __str__(self): return self.title
