from django.shortcuts import get_object_or_404
from rest_framework import serializers, exceptions
from rest_framework.authtoken.views import Token
from .models import UserAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'name', 'date_of_birth', 'password']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }

    def create(self, validated_data):
        user = UserAccount(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class TokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            if '@' in email_or_username:
                if email_or_username.count('@') != 1:
                    raise exceptions.ValidationError('Invalid value')
                user = get_object_or_404(UserAccount, email=email_or_username)
            else:
                user = get_object_or_404(UserAccount, name=email_or_username)

            if user:
                if not user.is_active:
                    raise exceptions.ValidationError('User account is disabled.')
            else:
                raise exceptions.ValidationError('Unable to log in with provided credentials.')
        else:
            raise exceptions.ValidationError('Must include "email or username" and "password"')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        super().create(validated_data)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
