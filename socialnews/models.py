from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Item(TimeStampedModel):
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=2000, blank=True, null=True)
    item_body_text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ItemComment(TimeStampedModel):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_comment = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.item_comment[:100]
