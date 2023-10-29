from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'User({self.id}, "{self.email}")'

    @staticmethod
    def is_email_valid(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def is_password_valid(passwd):
        if len(passwd) < 6:
            return False
        return True
