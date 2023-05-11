from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from CryptoTradingApp.core.validators import validate_image_size


UserModel = get_user_model()


class CryptoCurrency(models.Model):
    CRYPTO_NAME_MAX_LEN = 30
    DESCRIPTION_MAX_LEN = 300

    name = models.CharField(
        max_length=CRYPTO_NAME_MAX_LEN,
        null=False,
        blank=False
    )

    photo = models.ImageField(
        upload_to='crypto_photos/',
        validators=(validate_image_size,),
        null=False,
        blank=True
    )

    price = models.FloatField(
        null=False,
        blank=False,
        validators=(MinValueValidator(0),)
    )

    quantity = models.FloatField(
        null=False,
        blank=False,
        validators=(MinValueValidator(0.0000001),)
    )

    description = models.CharField(
        max_length=DESCRIPTION_MAX_LEN,
        null=True,
        blank=True
    )

    creator = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    date_of_creation = models.DateField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.name}')

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id}; Name: {self.name}"


class CryptoWallet(models.Model):
    balance = models.FloatField(
        null=False,
        blank=False,
        validators=(MinValueValidator(0),)
    )

    owner = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    crypto_inventory = models.ManyToManyField(CryptoCurrency, blank=True)

    def get_user_crypto(self):
        user_crypto_list = []

        for crypto in self.crypto_inventory.all():
            user_crypto_list.append((f"crypto_{crypto.name}", crypto.name))

        return user_crypto_list

    def __str__(self):
        return f"Wallet-{self.id};"
