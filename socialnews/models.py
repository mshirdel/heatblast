from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

from django_jalali.db import models as jmodels
from taggit.managers import TaggableManager

from .utils import get_domain


class TimeStampedModel(models.Model):
    objects = jmodels.jManager()
    created = jmodels.jDateTimeField(auto_now_add=True)
    modified = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Story(TimeStampedModel):
    objects = models.Manager()
    stories = StoryManager()

    title = models.CharField(max_length=500)
    url = models.URLField(max_length=2000, blank=True, null=True)
    story_body_text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
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
        if self.url:
            self.url_domain_name = get_domain(self.url)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("socialnews:show_story", args=[self.id])


class StoryComment(TimeStampedModel):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.story.update_number_of_votes()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.story.update_number_of_votes()


class Profile(models.Model):
    objects = jmodels.jManager()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user: {self.user.username}'