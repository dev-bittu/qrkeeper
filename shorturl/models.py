from django.db import models
from accounts.models import User
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from os.path import join
import qrcode

# Create your models here.
class ShortUrl(models.Model):
    long_url = models.URLField()
    slug = models.SlugField(unique=True, editable=False)
    qr = models.ImageField(upload_to="qr/%Y/%m/%d/", editable=False)
    visits = models.IntegerField(default=0)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Url({self.slug}, {self.long_url})"

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = self.random_slug(settings.GLOBAL_SETTINGS["short_url_slug_length"])
            self.slug = slug
        if not self.pk:
            self.qr = type(self).create_qr_code(self.slug)
        super(type(self), self).save(*args, **kwargs)

    def random_slug(self, length=5):
        slug = get_random_string(length)
        while type(self).objects.filter(slug=slug).exists():
            slug = get_random_string(length)
        return slug

    @staticmethod
    def is_url_valid(url):
        validator = URLValidator()
        try:
            validator(url)
            return True
        except ValidationError:
            return False

    @staticmethod
    def create_qr_code(slug):
        file = join(settings.BASE_DIR, "uploads", get_random_string(7)+".png")
        features = qrcode.QRCode(version=1, box_size=20, border=3)
        features.add_data(f"{settings.GLOBAL_SETTINGS['host']}/url/{slug}/")
        features.make(fit=True)
        img = features.make_image(
            fill_color="black",
            back_color="white"
        )
        img.save(file)
        return file
