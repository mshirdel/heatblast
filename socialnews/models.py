from django.db import models
from django.contrib.auth.models import User

from django_jalali.db import models as jmodels


class TimeStampedModel(models.Model):
    objects = jmodels.jManager()
    created = jmodels.jDateTimeField(auto_now_add=True)
    modified = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Story(TimeStampedModel):
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=2000, blank=True, null=True)
    story_body_text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class StoryComment(TimeStampedModel):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    story_comment = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.story_comment[:100]
