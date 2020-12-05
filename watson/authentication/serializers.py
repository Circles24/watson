from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_username(self, username):
        
        if User.objects.filter(username=username).count() > 0:
            raise serializers.ValidationError(f'username {username} already present')
        return username

    def validate_email(self, email):
        
        if User.objects.filter(email=email).count() > 0:
            raise serializers.ValidationError(f'email {email} already present')
        return email
    
    def save(self):
        User.objects.create_user(username=self.validated_data['username'],
                email=self.validated_data['email'],
                password=self.validated_data['password'])
