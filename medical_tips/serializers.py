from rest_framework import serializers
from .models import MedicalTip

class MedicalTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTip
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['created_at', 'updated_at'] 