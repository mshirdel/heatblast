import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
# from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
#                                         PermissionsMixin)
from django.contrib.auth.models import User
# from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.template import loader
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels
from taggit.managers import TaggableManager

from .utils import get_domain


class TimeStampedModel(models.Model):
    objects = jmodels.jManager()
    created = jmodels.jDateTimeField(auto_now_add=True)
    modified = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SocialUser(User):
    class Meta:
        proxy = True

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'expire': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class StoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Story(TimeStampedModel):
    objects = models.Manager()
    stories = StoryManager()

    title = models.CharField(_('title'), max_length=500)
    story_url = models.URLField(
        _('url'), max_length=2000, blank=True, null=True)
    story_body_text = models.TextField(
        _('sotry body text (use markdown)'), blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stories'
    )
    deleted = models.BooleanField(default=False)
    number_of_comments = models.IntegerField(default=0)
    number_of_votes = models.IntegerField(default=0)
    url_domain_name = models.CharField(max_length=500, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def update_number_of_comments(self):
        self.number_of_comments = self.comments.count()
        self.save()

    def update_number_of_votes(self):
        self.number_of_votes = self.storypoint_set.count()
        self.save()

    def save(self, *args, **kwargs):
        if self.story_url:
            self.url_domain_name = get_domain(self.story_url)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("socialnews:show_story", args=[self.id])


class StoryComment(TimeStampedModel):
    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name='comments')
    story_comment = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.story_comment[:100]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the real save() method
        self.story.update_number_of_comments()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.story.update_number_of_comments()


class StoryPoint(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.story.update_number_of_votes()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.story.update_number_of_votes()


class Profile(models.Model):
    objects = jmodels.jManager()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    activation_code = models.UUIDField(default=uuid.uuid4)
    token = models.UUIDField(default=uuid.uuid4)

    def send_activation_code(self, request, use_https=False):
        """
        Send activation code to user's email
        """
        current_site = get_current_site(request)
        message = loader.render_to_string(
            'socialnews/profile/activation_email.html', {
                'code': self.activation_code,
                'domain': current_site.domain,
                'protocol': 'https' if use_https else 'http',
                'token': self.token
            })
        send_mail(
            'Activating your account',
            message,
            'info@byteland.ir',
            [self.user.email],
            fail_silently=False,
        )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
