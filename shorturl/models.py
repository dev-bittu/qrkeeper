from django.db import models
from accounts.models import User
from django.utils.crypto import get_random_string

# Create your models here.
class ShortUrl(models.Model):
    long_url = models.URLField()
    slug = models.SlugField(unique=True)
    visits = models.IntegerField(default=0)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Url({self.slug}, {self.long_url})"

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = self.random_slug()
            self.slug = slug
        super(type(self), self).save(*args, **kwargs)

    def random_slug(self, length=5):
        slug = get_random_string(length)
        while type(self).objects.filter(slug=slug).exists():
            slug = get_random_string(length)
        return slug
