from rest_framework import serializers
from .models import VoiceQuery

class VoiceQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceQuery
        fields = '__all__'