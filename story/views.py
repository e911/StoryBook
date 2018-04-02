from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from story.models import Story, Response, Rating
from account.models import Author, Data
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
        user_list = Author.objects.all()
        query = request.GET.get("q")
        kind = request.GET.get("c")
        if query:
            if kind=='Story':
                stories_list = stories_list.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(content__icontains=query)
                    ).distinct()
            elif kind=='User':
                stories_list = stories_list.filter(
                    Q(author__user__username__icontains=query) |
                    Q(author__user__first_name__icontains=query) |
                    Q(author__user__last_name__icontains=query)
                    ).distinct()
            elif kind=='Tags':
                stories_list = stories_list.filter(
                    Q(tag__icontains=query)
                    ).distinct()
            else:
                stories_list = stories_list.filter(
                    Q(category__icontains=query)
                    ).distinct()

        paginator = Paginator(stories_list, 4) # Show 25 contacts per page
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
            'kind':kind,
        }
        return render(request,'story/home.html',context)

class Trending(View):
    def get(self, request):
        rating = Rating.objects.filter(rating=5)
        id= []
        for object in rating:
            id.append(object.story.id)
        id = set(id)
        stories_list = Story.objects.filter(id__in = id)

        paginator = Paginator(stories_list, 4) # Show 25 contacts per page
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
        data = Data.objects.all().first()
        author = Author.objects.get(user=request.user)
        if author.user.username in data.data:
            author.recommended_stories()
            stories_list = Story.objects.all()[:10]
        else:
            rating = Rating.objects.filter(rating=5)
            id= []
            for object in rating:
                id.append(object.story.id)
            id = set(id)
            stories_list = Story.objects.filter(id__in = id)
        paginator = Paginator(stories_list, 4) # Show 25 contacts per page
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


