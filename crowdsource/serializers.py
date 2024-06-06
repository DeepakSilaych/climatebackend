from rest_framework import serializers
from .models import CSFormData

class CSFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSFormData
        fields = '__all__'