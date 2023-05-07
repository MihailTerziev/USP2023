from django import forms
from django.shortcuts import render
from CryptoTradingApp.common.models import *
from CryptoTradingApp.crypto.models import *
from CryptoTradingApp.core.utils import *


class SearchCryptoForm(forms.Form):
    search_crypto_currencies_by_name = forms.CharField(max_length=50, required=False)


class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = CryptoPurchase
        fields = ("currency", "quantity", "payment_method")

        labels = {
            "currency": "Choose currency",
            "payment_method": "Choose payment method"
        }

        widgets = {
            "quantity": forms.NumberInput(
                attrs={
                    "placeholder": "Enter amount"
                }
            )
        }

    def create_purchase(self, request):
        purchase = super().save(commit=False)
        error_message = None

        crypto = CryptoCurrency.objects.filter(name__exact=purchase.currency).get()
        wallet = CryptoWallet.objects.filter(pk=request.user.pk).get()

        if purchase.payment_method == "wallet_balance":
            if wallet.balance >= crypto.price:
                wallet.balance -= crypto.price * purchase.quantity
            else:
                error_message = "You don't have enough in your balance to purchase this crypto!!!"

        if error_message is None:
            is_added = False

            for crypto_currency in wallet.crypto_inventory.all():
                if crypto_currency.name == crypto.name:
                    is_added = True
                    break

            if not is_added:
                wallet.crypto_inventory.add(crypto)

            crypto.quantity -= purchase.quantity
            purchase.buyer = request.user

            crypto.save()
            wallet.save()
            purchase.save()

        return error_message


class SaleCreateForm(forms.ModelForm):
    class Meta:
        model = CryptoSale
        fields = ("buyer", "currency", "quantity")

        labels = {
            "currency": "Choose currency",
            "quantity": "Amount of coins to sell"
        }

        widgets = {
            "quantity": forms.NumberInput(
                attrs={
                    "placeholder": "Enter amount"
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["buyer"].queryset = UserModel.objects.all()

    def create_sale(self, request):
        sale = super().save(commit=False)
        error_message = None

        sale.seller = request.user
        seller_wallet = CryptoWallet.objects.filter(pk=request.user.pk).get()
        buyer_wallet = CryptoWallet.objects.filter(pk=sale.buyer.pk).get()
        sold_crypto = CryptoCurrency.objects.filter(name__exact=sale.currency).get()

        seller_purchases = CryptoPurchase.objects.filter(buyer_id=request.user.pk)
        seller_trades = CryptoTrade.objects.filter(trader_id=request.user.pk)
        seller_sales = CryptoSale.objects.all()

        if check_if_crypto_in_user_wallet(sale.currency, seller_wallet.crypto_inventory.all()):
            owned_quantity = get_owned_crypto_quantity(request.user.pk, sale.currency, seller_purchases, seller_trades, seller_sales)

            if sale.quantity <= owned_quantity:
                buyer_wallet.balance -= sold_crypto.price * sale.quantity
                seller_wallet.balance += sold_crypto.price * sale.quantity

                if sold_crypto not in buyer_wallet.crypto_inventory.all():
                    buyer_wallet.crypto_inventory.add(sold_crypto)
            else:
                error_message = f"You don't own {sale.quantity} {sold_crypto.name}!!! Select less coins."
        else:
            error_message = f"You don't own {sold_crypto.name}!!!"

        if error_message is None:
            seller_wallet.save()
            buyer_wallet.save()
            sale.save()

        return error_message


class TradeCreateForm(forms.ModelForm):
    class Meta:
        model = CryptoTrade
        fields = ("traded_currency_one", "traded_currency_two", "traded_quantity")

        labels = {
            "traded_currency_one": "Convert",
            "traded_currency_two": "To",
            "traded_quantity": "Amount"
        }

        widgets = {
            "traded_quantity": forms.NumberInput(
                attrs={
                    "placeholder": "Enter amount"
                }
            )
        }

    def create_trade(self, request):
        trade = super().save(commit=False)

        error_message = None
        trader_owns_crypto = None

        trade.trader_wallet = CryptoWallet.objects.filter(pk=request.user.pk).get()
        trade.trader = request.user

        user_purchases = CryptoPurchase.objects.filter(buyer_id=request.user.pk)
        user_trades = CryptoTrade.objects.filter(trader_id=request.user.pk)
        user_sales = CryptoSale.objects.all()
        user_crypto = get_user_crypto_objects_list(request.user.pk, user_purchases, user_trades, user_sales)

        converted_to_crypto = CryptoCurrency.objects.filter(name__exact=trade.traded_currency_two).get()

        for converted_from_crypto, _ in user_crypto:
            if converted_from_crypto.name == trade.traded_currency_one:
                convert_ratio = converted_from_crypto.price / converted_to_crypto.price

                trade.converted_from_quantity = -trade.traded_quantity
                trade.converted_to_quantity = trade.traded_quantity * convert_ratio

                if not check_if_crypto_in_user_wallet(converted_to_crypto.name,
                                                      trade.trader_wallet.crypto_inventory.all()):
                    trade.trader_wallet.crypto_inventory.add(converted_to_crypto)
                    trade.trader_wallet.save()

                trader_owns_crypto = True
                break
            else:
                trader_owns_crypto = False

        if not trader_owns_crypto:
            error_message = f"You don't own {trade.traded_currency_one} to convert it in {trade.traded_currency_two}!!!"

        if error_message is None:
            trade.save()

        return error_message
