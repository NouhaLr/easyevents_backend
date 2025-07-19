
from rest_framework import serializers
from .models import  Event


from rest_framework import serializers
from .models import Event
from datetime import datetime

class EventSerializer(serializers.ModelSerializer):
    event_date = serializers.DateField(write_only=True)
    event_time = serializers.TimeField(write_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'place', 'description', 'image', 'plan',
            'normal_ticket_price', 'vip_ticket_price', 'created_at',
            'event_date', 'event_time',  # Input fields
            'date'  # Final combined datetime
        ]
        read_only_fields = ['date', 'created_at']

    def create(self, validated_data):
        event_date = validated_data.pop('event_date')
        event_time = validated_data.pop('event_time')
        combined_datetime = datetime.combine(event_date, event_time)
        validated_data['date'] = combined_datetime
        return super().create(validated_data)
