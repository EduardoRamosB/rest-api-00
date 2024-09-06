from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'password', 'created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'password', 'password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError('Passwords do not match')

        password = attrs.get('password', '')
        if len(password) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters')

        return attrs

    def create(self, validated_data):
        print('UserRegistrationSerializer.create validated_data after pop:', validated_data)
        validated_data.pop('password_confirmation', None)
        print('UserRegistrationSerializer.create validated_data before pop:', validated_data)
        user = CustomUser.objects.create_user(**validated_data)
        print('UserRegistrationSerializer.create user:', user)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(**attrs)

        if user and user.is_active:
            return user
        raise serializers.ValidationError('User is not active or credentials invalid')
