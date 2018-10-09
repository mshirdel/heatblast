from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from .models import Item
from .forms import StoryForm


class Stories(View):
    def get(self, request):
        return render(request, 'socialnews/index.html', {'items': Item.objects.all()})


class NewStory(View):
    def get(self, request):
        form = StoryForm()
        return render(request, 'socialnews/new_story.html', {'form': form})

    def post(self, request):
        form = StoryForm(request.POST)
        if form.is_valid():
            item = Item(title=form.cleaned_data['title'],
                        url=form.cleaned_data['url'],
                        item_body_text=form.cleaned_data['item_body_text'],
                        user=request.user
                        )
            item.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/new_story.html', {'form': form})


class EditStory(View):
    def get(self, request, id):
        item = Item.objects.get(pk=id)
        form = StoryForm(instance=item)
        return render(request, 'socialnews/edit_story.html', {'form': form, 'id': id})

    def post(self, request, id):
        item = Item.objects.get(pk=id)
        form = StoryForm(request.POST, instance=item)
        if form.is_valid():
            item.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'socialnews/edit_story.html', {'form': form, 'id': id})


class PanelView(View):
    def get(self, request):
        return render(request, 'socialnews/panel.html')

class ProfileView(View):
    def get(self, request):
        return render(request, 'socialnews/profile.html')
