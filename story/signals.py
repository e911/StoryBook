from json import dumps
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .utils import tokenize
from .models import Story, Response, Rating, Data, Frequency


@receiver(pre_save, sender=Story)
def create_slug(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug

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


