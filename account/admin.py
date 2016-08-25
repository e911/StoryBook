from django.contrib import admin
from .models import Author, Message, Notification
# Register your models here.

admin.site.register(Author)
admin.site.register(Message)
admin.site.register(Notification)
