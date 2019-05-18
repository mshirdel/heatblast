from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Story


class LatesStoryFeed(Feed):
    title = 'Heatblast'
    link = '/story/'
    description = 'New stories'

    def items(self):
        return Story.stories.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.story_body_text, 30)
