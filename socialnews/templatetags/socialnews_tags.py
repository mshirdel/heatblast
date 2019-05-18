from django.template import Library

from socialnews.models import Story

register = Library()

@register.simple_tag
def total_stories():
    return Story.objects.count()


@register.inclusion_tag('socialnews/templatetags/latest_stories.html')
def show_latest_stories(count=5):
    latest_stories = Story.stories.order_by('-created')[:count]
    return {'stories': latest_stories}
