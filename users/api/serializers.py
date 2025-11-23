from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT token serializer with custom claims"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        return token


class LoginSerializer(serializers.Serializer):
    """Login serializer for mobile app"""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Kullanıcı adı veya şifre hatalı.")
            if not user.is_active:
                raise serializers.ValidationError("Kullanıcı hesabı aktif değil.")
            attrs["user"] = user
        else:
            raise serializers.ValidationError("Kullanıcı adı ve şifre gereklidir.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """User serializer for API responses"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "username", "email", "first_name", "last_name"]

