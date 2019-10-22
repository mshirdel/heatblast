from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Story, SocialUser
from taggit.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'url']


class StorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Story
        fields = ['url_domain_name', 'title', 'story_url', 'story_body_text',
                  'user', 'number_of_comments', 'number_of_votes']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                _('An email address is required to log in.')
            )
        if password is None:
            raise serializers.ValidationError(
                _('A password is required to log in.')
            )
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                _('A user with this email and password was not found.')
            )
        if not user.is_active:
            raise serializers.ValidationError(
                _('This user has been deactivated.')
            )
        current_user = SocialUser.objects.get(pk=user.id)
        return {
            'email': user.email,
            'username': user.username,
            'token': current_user.token,
        }
