from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .forms import SignupForm, SigninForm, UserForm, ProfileForm, MessageForm
from django.contrib import messages
from .models import Author
from story.models import Story
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Signup(View):
    def get(self, request):
        form = SignupForm()
        context = {
            'form' : form,
        }
        return render(request, 'account/signup.html', context)

    def post(self, request):
        form = SignupForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = user.password
            user.set_password(password)
            user.save()

            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect ('story:home')
        context = {
            'registration_form':registration_form,
        }
        return render(request, 'account/register.html', context)

class Signin(View):
    def get(self, request):
        form = SigninForm()
        context = {
            'form' : form,
        }
        return render(request, 'account/signin.html', context)

    def post(self, request):
        form = SigninForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect ('story:home')
        else:
            print(form.errors)

        context = {
            'form' : form,
        }
        return render(request, 'account/signin.html', context)


class Signout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged Out Succesfully")
        return redirect ('story:index')


class Profile(View):
    def get(self, request, slug=None):
        instance = get_object_or_404(Author, slug=slug)
        follower = len(instance.follower)
        following = len(instance.following)
        stories_list = Story.objects.filter(author=instance)

        paginator = Paginator(stories_list, 3) # Show 25 contacts per page
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
            'instance': instance,
            'follower': follower,
            'following': following,
        }
        return render(request, 'account/profile.html', context)

    def post(self, request, slug=None):
        instance = get_object_or_404(Author, slug=slug)
        instance2 = get_object_or_404(Author, user=request.user)

        follower = len(instance.follower)
        following = len(instance.following)

        if request.user != instance.user:
            if request.user.username not in instance.follower:
                instance.follower.append(request.user.username)
                instance.save()
            else:
                instance.follower.remove(request.user.username)
                instance.save()

            if instance.user.username not in instance2.following:
                instance2.following.append(instance.user.username)
                instance2.save()
            else:
                instance2.following.remove(instance.user.username)
                instance2.save()


            return redirect(instance.get_absolute_url())

        context = {
            'instance': instance,
            'follower': follower,
            'following': following,
        }
        return render(request, 'account/profile.html', context)


class Update(View):
    def get(self, request, slug=None):
        instance = get_object_or_404(Author, slug=slug)
        user_form = UserForm(instance=instance.user)
        profile_form = ProfileForm(instance=instance)
        context = {
            "instance": instance,
            "user_form": user_form,
            "profile_form": profile_form,
        }
        return render(request, "account/update.html", context)

    def post(self, request, slug=None):
        instance = get_object_or_404(Author, slug=slug)
        user_form = UserForm(request.POST or None, instance=instance.user)
        profile_form = ProfileForm(
            request.POST or None, request.FILES or None, instance=instance)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            print(user_form.errors, profile_form.errors)

        context = {
            "instance": instance,

        }

        return render(request, 'account/update.html', context)
