from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from CryptoTradingApp.core.validators import validate_image_size


class AppUser(AbstractUser):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 30
    PHONE_MAX_LEN = 15

    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(MinLengthValidator(MIN_NAME_LENGTH),)
    )

    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(MinLengthValidator(MIN_NAME_LENGTH),)
    )

    photo = models.ImageField(
        upload_to='users_photos/',
        validators=(validate_image_size,),
        null=False,
        blank=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=PHONE_MAX_LEN,
        null=False,
        blank=False
    )
