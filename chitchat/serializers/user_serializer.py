from rest_framework import serializers
from chitchat.models.user_models import User
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password:
            if password != confirm_password:
                raise serializers.ValidationError("Passwords provided were different")
        return super().validate(attrs)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        _ = validated_data.pop("confirm_password", None)
        instance.set_password(password)
        # Update other fields (e.g., full_name)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance