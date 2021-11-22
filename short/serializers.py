from .models import URL
from rest_framework import serializers
class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model=URL
        fields='__all__'