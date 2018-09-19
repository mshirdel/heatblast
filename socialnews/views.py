from django.shortcuts import render
from django.http import HttpResponse

from .models import Item


def index(request):
    return render(request, 'socialnews/index.html', {'items': Item.objects.all()})
