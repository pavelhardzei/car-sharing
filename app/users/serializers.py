from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.views import Token
from .models import UserAccount
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'name', 'date_of_birth', 'password')

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_date_of_birth(self, value):
        if (datetime.now() - datetime.strptime(str(value), '%Y-%m-%d')).days // 365 < 18:
            raise ValidationError({'error_message': 'Age must be >= 18'})
        return value

    def create(self, validated_data):
        user = UserAccount(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('email', 'name')


class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_rep = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ('old_password', 'password', 'password_rep')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_rep']:
            raise ValidationError({'message_error': 'Passwords did not match'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError({'message_error': 'Old password is not correct'})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        name = attrs.get('name')
        password = attrs.get('password')

        if email and name or not password or not email and not name:
            raise ValidationError({'error_message': 'Must include email + pwd or name + pwd'})

        if email:
            user = get_object_or_404(UserAccount, email=email)
        else:
            user = get_object_or_404(UserAccount, name=name)

        user = authenticate(email=user.email, password=password)
        if user:
            if not user.is_active:
                raise ValidationError({'error_message': 'User account is disabled'})
        else:
            raise ValidationError({'error_message': 'Unable to log in with provided credentials'})

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        super().create(validated_data)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
