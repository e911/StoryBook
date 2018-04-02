from django.conf.urls import url
from . import signals

from .views import *


urlpatterns = [
    url(r'^accounts/signup/$', Signup.as_view(), name='signup'),
    url(r'^accounts/signin/$', Signin.as_view(), name='signin'),
    url(r'^accounts/signout/$', Signout.as_view(), name='signout'),
    url(r'^@(?P<slug>[\w-]+)/$', Profile.as_view(), name="profile"),
    url(r'^@(?P<slug>[\w-]+)/update/$', Update.as_view(), name="update"),




]
