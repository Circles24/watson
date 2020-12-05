from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import register

urlpatterns = [
        path('login', TokenObtainPairView.as_view(), name='login'),
        path('register', register, name='register')
        ]
