from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver
from CryptoTradingApp.crypto.models import CryptoWallet
from CryptoTradingApp.common.models import *


UserModel = get_user_model()


@receiver(signals.post_save, sender=UserModel)
def add_wallet_when_user_is_created(instance, created, *args, **kwargs):
    if not created:
        return

    CryptoWallet.objects.create(
        pk=instance.pk,
        owner_id=instance.pk,
        balance=0.00,
    )
