from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField,JSONField
from .utils import recommend_gradient, recommend_knn


# Create your models here.

class Timestampable(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` , ``updated`` and  ``deleted``
    field.
    """
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


    def delete(self):
        self.deleted_at = timezone.now()
        self.deleted = True
        super().save()

GENDER_CHOCIES = (
    (0, 'Not Known'),
    (1, 'Male'),
    (2, 'Female'),
    (9, 'Others'),
)


def upload_location(instance, filename):
    return "%s/%s/%s" % ('users', instance.user.username, filename)


class Author(Timestampable):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=upload_location,
                              null=True,
                              height_field='height',
                              width_field='width',
                              blank=True)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    bio = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    gender = models.PositiveIntegerField(default=0, choices=GENDER_CHOCIES)
    follower = ArrayField(models.CharField(
        max_length=255, blank=True), null=True, blank=True)
    following = ArrayField(models.CharField(
        max_length=255, blank=True), null=True, blank=True)

    def get_absolute_url(self):
        return reverse("user:profile", kwargs={"slug": self.slug})

    def __str__(self):
        return self.user.username

    def recommended_stories(self):
        data = Data.objects.all().first()
        my_prediction, story_list = recommend_gradient(self.user.username, data)
        recommended = recommend_knn(self.user.username, data,'Pearson')



class Data(models.Model):
    data = JSONField()

    def __str__(self):
        return 'Training data'


class Message(Timestampable):
    sender = models.ForeignKey(Author, related_name='Sender')
    receiver = models.ForeignKey(Author, related_name='Receiver')
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        text = "%s-%s-%s" % (self.sender.user.username,
                             self.receiver.user.username, self.id)
        return text


class Notification(Timestampable):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:30]

