from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

        def validate(self, attrs):
            if attrs['password'] != attrs['password_confirmation']:
                raise serializers.ValidationError('Passwords do not match')

            password = attrs.get('password', '')
            if len(password) < 8:
                raise serializers.ValidationError('Password must be at least 8 characters')

            return attrs

        def create(self, validated_data):
            # password = validated_data.pop('password', None)
            validated_data.pop('password_confirmation', None)

            return CustomUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(**attrs)

        if user and user.is_active:
            return user
        raise serializers.ValidationError('User is not active or credentials invalid')
