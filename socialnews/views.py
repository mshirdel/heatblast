from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from .models import Item


class Stories(View):
    def get(self, request):
        return render(request, 'socialnews/index.html', {'items': Item.objects.all()})


class PanelView(View):
    def get(self, request):
        return render(request, 'socialnews/panel.html')
