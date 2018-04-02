from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Author


@receiver(pre_save, sender=Author)
def create_slug(sender, instance, *args, **kwargs):
    slug = slugify(instance.user.username,)
    instance.slug = slug


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Author.objects.get_or_create(
            user=instance, follower=[], following=[])
