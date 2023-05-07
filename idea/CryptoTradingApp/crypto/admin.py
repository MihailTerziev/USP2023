from django.contrib import admin
from CryptoTradingApp.crypto.models import *


@admin.register(CryptoCurrency)
class CryptoCurrencyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'quantity', 'date_of_creation')


@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ('pk', 'all_crypto', 'owner')

    @staticmethod
    def all_crypto(obj: CryptoWallet):
        owned_crypto = obj.crypto_inventory.all()

        if owned_crypto:
            return ', '.join([currency.name for currency in owned_crypto])

        return "None"
