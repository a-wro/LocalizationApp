from rest_framework import serializers
from .models import UserEntry, ZipCodeCounter

class UserEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEntry
        fields = '__all__'

class ZipCodeCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipCodeCounter
        fields = '__all__'