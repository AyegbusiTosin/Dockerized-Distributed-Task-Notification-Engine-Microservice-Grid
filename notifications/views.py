from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import NotificationJob
from .serializers import NotificationJobSerializer
from .tasks import send_scheduled_email_task


class NotificationJobViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationJobSerializer

    #ensures only authenticated users are allowed
    permission_classes = [IsAuthenticated]

    #self.request.user tracks who is currently making the API request
    #.filter(owner=self.request.user)- this filters the database spreedsheet. User only see their row
    #.select_related('owner'): Adds SQL JOIN to pre-fetch user details in one go. Prevents N+1 Query Problem
    def get_queryset(self):
        return NotificationJob.objects.filter(owner=self.request.user).select_related('owner')

    #this ensures every task is attached to the user logged in
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        #send_scheduled_email_task.delay(job.id)
