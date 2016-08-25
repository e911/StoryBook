from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from story.models import Story, Response, Rating
from account.models import Author
from .forms import StoryForm, ResponseForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Create(View):
    def get(self, request, author_slug=None):
        author = get_object_or_404(Author, slug=author_slug)
        form = StoryForm()
        context = {
            'author':author,
            'form':form,
        }
        return render (request, 'story/create.html', context)

    def post(self, request, author_slug=None):
        author = get_object_or_404(Author, slug=author_slug)
        form = StoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = author
            if request.POST.get('draft','off')=='on':
                instance.draft = True
            else:
                instance.draft = False
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            'author':author,
            'form':form,
        }
        return render (request, 'story/create.html', context)


class Update(View):
    def get(self, request, story_slug=None):
        story = get_object_or_404(Story, slug = story_slug)
        form = StoryForm(instance = story)
        context = {
            'form':form,
            'story':story,
        }
        return render (request, 'story/update.html', context)

    def post(self, request, story_slug=None):
        story = get_object_or_404(Story, slug = story_slug)
        form = StoryForm(request.POST or None, request.FILES or None, instance=story)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.POST.get('draft','off')=='on':
                instance.draft = True
            else:
                instance.draft = False
            instance.save()
            return HttpResponseRedirect(story.get_absolute_url())

            context = {
            'form':form,
        }
        return render (request, 'story/update.html', context)

class Detail(View):

    def get(self, request, story_slug=None):
        story = get_object_or_404(Story, slug = story_slug)
        form = ResponseForm()
        context={
            'story':story,
            'form':form,
        }
        return render(request, 'story/detail.html', context)

    def post(self,request, story_slug=None):
        story = get_object_or_404(Story, slug = story_slug)
        form = ResponseForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.rating = request.POST.get('rating-input-1',0)
            instance.story = story
            instance.commenter = get_object_or_404(Author, user=request.user)
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None

            if parent_id:
                instance.rating = 0
                parent_qs = Response.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    instance.parent = parent_qs.first()
            instance.save()
            print(request.POST.get('rating-input-1',0), instance)
            return HttpResponseRedirect(story.get_absolute_url())
        else:
            print(form.errors)
        context={
            'story':story,
            'form':form,
        }
        return render(request, 'story/detail.html', context)


class Delete(View):
    def get(self,request, story_slug=None):
        story = get_object_or_404(Story, slug = story_slug)
        story.delete()
        return HttpResponseRedirect('/admin')

class Index(View):
    def get(self, request):
        stories = Story.objects.all()
        ids = []
        for story in stories:
            ids.append(story.id)
        print(ids)
        context = {
        }
        return render(request,'story/index.html',context)

class Home(View):
    def get(self, request):
        stories_list = Story.objects.all()
        query = request.GET.get("q")
        kind = request.GET.get("c")
        if kind=='Story':
            a = 'a'
        elif kind=='User':
            a = 'b'
        elif kind=='Tags':
            a = 'c'
        else:
            a = 'd'

        paginator = Paginator(stories_list, 1) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            stories = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            stories = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            stories = paginator.page(paginator.num_pages)

        tags, categories = [], []
        for story in stories_list:
            temp1, temp2 = set(tags) | set(story.tag), set(categories) |set(story.category)
            tags, categories = temp1, temp2

        tags, categories =list(tags), list(categories)

        context = {
            'stories':stories,
            'tags':tags,
            'categories':categories,
        }
        return render(request,'story/home.html',context)

class Trending(View):
    def get(self, request):
        stories_list = Story.objects.all()
        query = request.GET.get("q")
        kind = request.GET.get("c")
        if kind=='Story':
            a = 'a'
        elif kind=='User':
            a = 'b'
        elif kind=='Tags':
            a = 'c'
        else:
            a = 'd'

        paginator = Paginator(stories_list, 1) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            stories = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            stories = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            stories = paginator.page(paginator.num_pages)

        tags, categories = [], []
        for story in stories_list:
            temp1, temp2 = set(tags) | set(story.tag), set(categories) |set(story.category)
            tags, categories = temp1, temp2

        tags, categories =list(tags), list(categories)

        context = {
            'stories':stories,
            'tags':tags,
            'categories':categories,
        }
        return render(request,'story/trending.html',context)

class Recommended(View):
    def get(self, request):
        stories_list = Story.objects.all()
        query = request.GET.get("q")
        kind = request.GET.get("c")
        if kind=='Story':
            a = 'a'
        elif kind=='User':
            a = 'b'
        elif kind=='Tags':
            a = 'c'
        else:
            a = 'd'

        paginator = Paginator(stories_list, 1) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            stories = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            stories = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            stories = paginator.page(paginator.num_pages)

        tags, categories = [], []
        for story in stories_list:
            temp1, temp2 = set(tags) | set(story.tag), set(categories) |set(story.category)
            tags, categories = temp1, temp2

        tags, categories =list(tags), list(categories)

        context = {
            'stories':stories,
            'tags':tags,
            'categories':categories,
        }
        return render(request,'story/recommended.html',context)


class About(View):
    def get(self, request):
        context = {}
        return render(request,'about.html',context)

class Contact(View):
    def get(self, request):
        context = {}
        return render(request,'contact.html',context)


