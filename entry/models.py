from django.db import models
from django.conf import settings
from socialnews.models import TimeStampedModel


class Entry(TimeStampedModel):
    body_text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='entries')
