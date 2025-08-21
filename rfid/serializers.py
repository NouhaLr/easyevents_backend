# rfid/serializers.py
from rest_framework import serializers
from .models import Bracelet

class BraceletAssignSerializer(serializers.Serializer):
    receipt_number = serializers.CharField()
    tag_uid = serializers.CharField()

class BraceletSerializer(serializers.ModelSerializer):
    reservation = serializers.CharField(source='reservation.receipt_number', read_only=True)

    class Meta:
        model = Bracelet
        fields = ['id', 'reservation', 'tag_uid', 'active', 'issued_at']
