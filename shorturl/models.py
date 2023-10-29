from django.db import models
from accounts.models import User

# Create your models here.
class ShortUrl(models.Model):
    long_url = models.URLField()
    slug = models.SlugField()
    visits = models.IntegerField(default=0)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Url({self.slug}, {self.long_url})"
