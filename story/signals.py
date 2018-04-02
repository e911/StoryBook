from json import dumps, loads
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .utils import tokenize, read_time
from .models import Story, Response, Rating, Frequency
from account.models import Data



@receiver(pre_save, sender=Story)
def create_slug(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    time = read_time(instance.content)
    instance.slug = slug
    instance.read_time = time

@receiver(post_save, sender=Response)
def create_rating(sender, instance, *args, **kwargs):
    if instance.is_parent:
        rating = Rating.objects.filter(author=instance.commenter).filter(story= instance.story).first()
        if not rating :
            Rating.objects.create(author=instance.commenter,story= instance.story,rating =instance.rating)
        else:
            rating.rating = instance.rating
            rating.save()

@receiver(post_save, sender=Story)
def create_frequency(sender, instance, *args, **kwargs):
    terms = tokenize(instance.content)
    json = dumps(dict(terms))

    frequency = Frequency.objects.filter(story=instance).first()
    if frequency:
        frequency.tokens = json
        frequency.save()
    else:
        Frequency.objects.create(story=instance, tokens= json)


@receiver(post_save, sender=Rating)
def create_data(sender, instance, *args, **kwargs):
    temp = {}
    data = Data.objects.all().first()

    if data:
        temp = loads(data.data)
        if instance.author.user.username in temp.keys():
            temp[instance.author.user.username].setdefault(instance.story.title, 0)
            temp[instance.author.user.username][instance.story.title] = instance.rating
        else:
            temp.setdefault(instance.author.user.username,{})
            temp[instance.author.user.username].setdefault(instance.story.title, 0)
            temp[instance.author.user.username][instance.story.title] = instance.rating
        data.data = dumps(temp)
        data.save()
    else:
        temp.setdefault(instance.author.user.username,{})
        temp[instance.author.user.username].setdefault(instance.story.title, 0)
        temp[instance.author.user.username][instance.story.title] = instance.rating
        data = Data(data=dumps(temp))
        data.save()
