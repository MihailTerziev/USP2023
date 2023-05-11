from enum import Enum
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from CryptoTradingApp.crypto.models import *
from CryptoTradingApp.core.mixins import ChoicesEnumMixin
from CryptoTradingApp.core.utils import get_all_crypto, get_all_users


UserModel = get_user_model()


class PaymentMethod(ChoicesEnumMixin, Enum):
    mobile_payment = "Mobile payment"
    bank_transfer = "Electronic bank transfer"
    credit_card = "Credit Card"
    debit_card = "Debit Card"
    paypal = "PayPal"


class CryptoPurchase(models.Model):
    CURRENCY_MAX_LEN = 20

    date_of_purchase = models.DateField(
        auto_now_add=True,
    )

    quantity = models.FloatField(
        validators=(MinValueValidator(0.0000001),)
    )

    payment_method = models.CharField(
        choices=PaymentMethod.choices(add_wallet_balance=True),
        max_length=PaymentMethod.max_len(),
    )

    buyer = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    currency = models.CharField(
        choices=get_all_crypto(),
        max_length=CURRENCY_MAX_LEN,
    )

    def __str__(self):
        return f"ID: {self.id}; Buyer: {self.buyer.first_name} {self.buyer.last_name};" \
               f" Crypto: {self.currency.name}; quantity: {self.quantity}; Payment: {self.payment_method}"


class CryptoSale(models.Model):
    CURRENCY_MAX_LEN = 20

    date_of_sale = models.DateField(
        auto_now_add=True,
    )

    quantity = models.FloatField(
        validators=(MinValueValidator(0.0000001),)
    )

    seller = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
        related_name="seller"
    )

    buyer = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
        related_name="buyer"
    )

    currency = models.CharField(
        choices=get_all_crypto(),
        max_length=CURRENCY_MAX_LEN,
    )

    def __str__(self):
        return f"ID: {self.id}; " \
               f"Seller: {self.seller.first_name} {self.seller.last_name}; " \
               f"Buyer: {self.buyer.first_name} {self.buyer.last_name}; " \
               f"Crypto: {self.currency.name}; quantity: {self.quantity};"


class CryptoTrade(models.Model):
    CURRENCY_MAX_LEN = 20

    traded_currency_one = models.CharField(
        choices=get_all_crypto(),
        max_length=CURRENCY_MAX_LEN,
    )

    traded_currency_two = models.CharField(
        choices=get_all_crypto(),
        max_length=CURRENCY_MAX_LEN,
    )

    traded_quantity = models.FloatField(
        null=False,
        blank=False,
        validators=(MinValueValidator(0.0000001),)
    )

    converted_from_quantity = models.FloatField(
        null=False,
        blank=False
    )

    converted_to_quantity = models.FloatField(
        null=False,
        blank=False,
        validators=(MinValueValidator(0.0000001),)
    )

    date_of_trade = models.DateField(
        auto_now_add=True,
        null=False,
        blank=True
    )

    trader = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    trader_wallet = models.ForeignKey(
        CryptoWallet,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return f"ID: {self.id}; Trader: {self.trader.first_name} {self.trader.last_name};" \
               f" Crypto: {self.traded_currency.name}; quantity: {self.traded_quantity};"


class BalanceIncrease(models.Model):
    amount = models.FloatField(
        validators=(MinValueValidator(10),)
    )

    transaction_method = models.CharField(
        choices=PaymentMethod.choices(),
        max_length=PaymentMethod.max_len(),
    )

    date_of_transaction = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )
