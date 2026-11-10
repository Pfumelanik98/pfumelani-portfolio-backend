from django.contrib import admin
from .models import Education, Certificate, Resume

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("qualification", "institution", "status", "start_year", "end_year")

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "issue_date", "is_published")
    list_filter = ("is_published",)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "version", "is_active", "uploaded_at")
