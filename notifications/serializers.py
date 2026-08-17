from rest_framework import serializers
from .models import NotificationJob
from django.utils import timezone

#the serializer filters,validates, converts JSON payload before saving to database
class NotificationJobSerializer(serializers.ModelSerializer):
    scheduled_time = serializers.DateTimeField()


    class Meta:
        model = NotificationJob

        #fields expected in the JSON payload and frontend 
        fields = ['id', 'title', 'message', 'recipient_email', 'scheduled_time', 'status', 'created_at', 'secret_key']

        #fields that can be seen (GET), but not editable (POST)
        read_only_fields = ['id', 'status', 'created_at']

        #field can be written (POST), but will not be shown (GET)
        #'secret_key'  is now excluded
        #'created_at' can be seen but not editable
        extra_kwargs = {
            'secret_key': {'write_only' : True},
            'created_at' :{'read_only'  : True}
        }

        #validate time input logic
    def validate_scheduled_time(self,value):
        
        if value < timezone.now():
            raise serializers.ValidationError("The scheduled time must be in the future!.")
        return value