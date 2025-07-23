from rest_framework import serializers
from .models import AppUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role

        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'username': {'required': False}}

    def create(self, validated_data):
        username = validated_data.get('username') or validated_data['email'].split('@')[0]
        user = AppUser.objects.create(
            username=username,
            email=validated_data['email'],
            role='attender'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'role')

class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
