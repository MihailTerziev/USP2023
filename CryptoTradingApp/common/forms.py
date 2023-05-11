from django import forms
from CryptoTradingApp.common.models import *
from CryptoTradingApp.crypto.models import *
from CryptoTradingApp.core.utils import get_user_crypto_objects_list, check_if_crypto_in_user_wallet


class IncreaseBalanceForm(forms.Form):
    amount = forms.CharField(widget=forms.NumberInput)
    transaction_method = forms.ChoiceField(choices=PaymentMethod.choices())


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

    def create_purchase(self, user):  # TODO implement exception handling
        purchase = super().save(commit=False)

        crypto = CryptoCurrency.objects.filter(name__exact=purchase.currency).get()
        wallet = CryptoWallet.objects.filter(pk=user.pk).get()

        # TODO if payment method is not crypto wallet don't change balance
        if wallet.balance >= crypto.price:
            wallet.balance -= crypto.price * purchase.quantity

            is_added = False

            for crypto_currency in wallet.crypto_inventory.all():
                if crypto_currency.name == crypto.name:
                    is_added = True
                    break

            if not is_added:
                wallet.crypto_inventory.add(crypto)

            crypto.quantity -= purchase.quantity
            purchase.buyer = user

            crypto.save()
            wallet.save()
            purchase.save()
        else:
            # TODO raise error
            return


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

    def create_sale(self, user):  # TODO implement exception handling
        sale = super().save(commit=False)

        sale.seller = user
        seller_wallet = CryptoWallet.objects.filter(pk=user.pk).get()
        buyer_wallet = CryptoWallet.objects.filter(pk=sale.buyer.pk).get()
        sold_crypto = CryptoCurrency.objects.filter(name__exact=sale.currency).get()

        if check_if_crypto_in_user_wallet(sale.currency, seller_wallet.crypto_inventory.all()):
            # TODO check if quantity is less than owned or raise error

            buyer_wallet.balance -= sold_crypto.price * sale.quantity
            seller_wallet.balance += sold_crypto.price * sale.quantity

            if sold_crypto not in buyer_wallet.crypto_inventory.all():
                buyer_wallet.crypto_inventory.add(sold_crypto)
        else:
            pass  # TODO raise an error

        seller_wallet.save()
        buyer_wallet.save()
        sale.save()


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

    def create_trade(self, user):  # TODO implement exception handling, if user chooses crypto he doesn't own
        trade = super().save(commit=False)

        trade.trader_wallet = CryptoWallet.objects.filter(pk=user.pk).get()
        trade.trader = user

        user_purchases = CryptoPurchase.objects.filter(buyer_id=user.pk)
        user_trades = CryptoTrade.objects.filter(trader_id=user.pk)
        user_sales = CryptoSale.objects.all()
        user_crypto = get_user_crypto_objects_list(user.pk, user_purchases, user_trades, user_sales)

        converted_to_crypto = CryptoCurrency.objects.filter(name__exact=trade.traded_currency_two).get()

        for converted_from_crypto, _ in user_crypto:
            if converted_from_crypto.name == trade.traded_currency_one:
                convert_ratio = converted_from_crypto.price / converted_to_crypto.price

                trade.converted_from_quantity = -trade.traded_quantity
                trade.converted_to_quantity = trade.traded_quantity * convert_ratio

                if not check_if_crypto_in_user_wallet(converted_to_crypto.name, trade.trader_wallet.crypto_inventory.all()):
                    trade.trader_wallet.crypto_inventory.add(converted_to_crypto)
                    trade.trader_wallet.save()

                break
            else:
                pass
            # TODO raise error

        trade.save()
