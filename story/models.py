from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from account.models import Timestampable, Author
from django.core.urlresolvers import reverse

# Create your models here.


class StoryManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(StoryManager, self).filter(draft=False).filter(deleted=False)



def story_photo(instance, filename):
    return "%s/%s/%s" % ('story', instance.title, filename)


class Story(Timestampable):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(upload_to=story_photo,
                              blank=True,
                              height_field='height',
                              width_field='width')
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    tag = ArrayField(models.CharField(
        max_length=255, blank=True), blank=True)
    category = ArrayField(models.CharField(
        max_length=255, blank=True), blank=True)
    draft = models.BooleanField(default=False, blank=True)
    objects = StoryManager()

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("story:detail", kwargs={"story_slug": self.slug})

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    @property
    def response(self):
        return Response.objects.filter(story=self).filter(parent=None)

    @property
    def responsecount(self):
        return Response.objects.filter(story=self).filter(parent=None).count()



class ResponseManager(models.Manager):
    def all(self):
        return super(ResponseManager, self).filter(parent=None)

RATING_CHOICE = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)
class Response(Timestampable):
    commenter = models.ForeignKey(Author, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 500)
    rating = models.FloatField(default=0, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,default=None)

    objects = ResponseManager()

    class Meta:
         ordering = ['-created_at','-updated_at']

    def __str__(self):
        return self.comment[:30]

    def children(self):  # replies
        return Response.objects.filter(parent=self)

    def children(self):  # replies
        return Response.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Rating(Timestampable):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    rating = models.FloatField(default=0, blank=True)

    def __str__(self):
       title ="{user}-{story}"
       return title.format(user=self.author.user.username, story=self.story.title)


class Data(models.Model):
    data = JSONField()

    def __str__(self):
        return 'Training data'


class Frequency(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    tokens = JSONField(null=True)

    def __str__(self):
        return self.story.title