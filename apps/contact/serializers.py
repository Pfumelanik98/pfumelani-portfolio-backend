from rest_framework import serializers
from .models import ContactMessage

class ContactMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "full_name", "email", "subject", "message", "created_at"]
        read_only_fields = ["id", "created_at"]
    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Please provide a little more detail (at least 10 characters).")
        return value.strip()
