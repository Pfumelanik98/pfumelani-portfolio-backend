from rest_framework import serializers
from .models import Education, Certificate, Resume

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["id", "institution", "qualification", "field_of_study", "start_year", "end_year", "status", "description", "display_order"]
        read_only_fields = ["id"]
    def validate(self, attrs):
        start = attrs.get("start_year", getattr(self.instance, "start_year", None))
        end = attrs.get("end_year", getattr(self.instance, "end_year", None))
        if end is not None and start is not None and end < start:
            raise serializers.ValidationError({"end_year": "End year cannot be earlier than start year."})
        return attrs

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "title", "issuer", "issue_date", "credential_url", "document", "is_published"]
        read_only_fields = ["id"]

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "title", "file", "version", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]
