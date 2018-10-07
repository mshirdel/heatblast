from django.contrib import admin
from .models import Item, ItemComment

from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


class ItemAdmin(admin.ModelAdmin):
    list_filter = (
        ('created', JDateFieldListFilter),
    )


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemComment)
