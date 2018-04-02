from django.contrib import admin
from .models import Author, Message, Notification, Data
# Register your models here.

admin.site.register(Author)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Data)
