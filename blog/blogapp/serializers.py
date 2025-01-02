from django.contrib.auth.models import User
from .models import Blog
from rest_framework import serializers

User.objects.filter(is_active=False).update(is_active=True)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Blog
        fields = "__all__"