from django.contrib.sitemaps import Sitemap
from .models import Story


class StorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Story.stories.all()

    def lastmod(self, obj):
        return obj.modified
