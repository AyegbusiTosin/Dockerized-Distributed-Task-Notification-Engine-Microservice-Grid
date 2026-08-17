from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationJobViewSet

#automatically builds the 5 API URL endpoints
#GET /api/jobs/
#POST /api/jobs/
#... 
router = DefaultRouter()

#'jobs' becomes the job prefix for all URL(api/'jobs'/)
router.register(r'jobs', NotificationJobViewSet, basename='notification-jobs')

#includes the router's generated paths into Django URL list
urlpatterns = [
    path('', include(router.urls))
]