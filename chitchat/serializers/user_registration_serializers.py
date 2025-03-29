from rest_framework import serializers
from chitchat.models.user_models import User
from django.db.models import Q


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("confirm_password"):
            raise serializers.ValidationError("Passwords provided were different")
        if User.objects.filter(
            Q(email=attrs["email"]) | Q(username=attrs["username"])
        ).exists():
            raise serializers.ValidationError("Username with Email already exists!")
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
