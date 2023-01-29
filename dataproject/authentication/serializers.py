
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    first_name = serializers.CharField(max_length=255, min_length=8)
    last_name = serializers.CharField(max_length=255, min_length=8)
    password = serializers.CharField(
        max_length=100, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('email already taken')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': ('username already taken')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(max_length=255, min_length=3)
    # username = serializers.CharField(max_length=255, min_length=8)
    password = serializers.CharField(
        max_length=100, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
        # required_only_fields = ['']
