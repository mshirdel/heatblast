from django.contrib import admin
from .models import Story, StoryComment, Profile

from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


class StoryAdmin(admin.ModelAdmin):
    list_filter = (
        ('created', JDateFieldListFilter),
    )


admin.site.register(Story, StoryAdmin)
admin.site.register(StoryComment)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
