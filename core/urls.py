"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny


class CookieExemptTokenObtainPairView(TokenObtainPairView):
    authentication_classes =()
    permission_classes = (AllowAny,)

class CookieExemptTokenRefreshView(TokenRefreshView):
    authentication_classes = ()
    permission_classes = (AllowAny,)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('notifications.urls')),


#secure JWT authentication gateway endpoints 
path('api/v1/auth/login/', CookieExemptTokenObtainPairView.as_view(), name='token_obtain_pair'),
path('api/v1/auth/refresh/', CookieExemptTokenRefreshView.as_view() , name='token_refresh'),

]