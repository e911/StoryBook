from django.conf.urls import url
from . import signals

from .views import *

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^aboutus/$', About.as_view(), name='about'),
    url(r'^contactus/$', Contact.as_view(), name='contact'),
    url(r'^story/trending/$', Trending.as_view(), name='trending'),
    url(r'^story/recommended/$', Recommended.as_view(), name='recommended'),
    url(r'^@(?P<author_slug>[\w-]+)/story/create/$',
        Create.as_view(), name='create'),
    url(r'^(?P<story_slug>[\w-]+)/update/$',
        Update.as_view(), name='update'),
    url(r'^(?P<story_slug>[\w-]+)/$',
        Detail.as_view(), name='detail'),
    url(r'^(?P<story_slug>[\w-]+)/delete$',
        Delete.as_view(), name='delete'),

]
