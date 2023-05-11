from CryptoTradingApp.crypto.models import *


def get_crypto_by_slug(crypto_slug):
    return CryptoCurrency.objects.get(slug=crypto_slug)


def get_all_users():
    return [(user, user.get_full_name()) for user in UserModel.objects.all()]


def check_if_crypto_in_user_wallet(crypto_name, wallet_inventory):
    for crypto in wallet_inventory:
        if crypto.name == crypto_name:
            return True

    return False


def get_all_crypto():
    all_crypto_list = []

    for crypto in CryptoCurrency.objects.all():
        all_crypto_list.append((crypto.name, crypto.name))

    return all_crypto_list


def get_user_crypto_str_list(user_pk):
    wallet = CryptoWallet.objects.filter(pk=user_pk).get()

    user_crypto_list = []

    for crypto in wallet.crypto_inventory.all():
        user_crypto_list.append([crypto.name, crypto.name])

    return user_crypto_list


def get_user_crypto_objects_list(user_pk, user_purchases, user_trades, user_sales):
    wallet = CryptoWallet.objects.filter(pk=user_pk).get()

    user_crypto_list = []

    for crypto in wallet.crypto_inventory.all():
        user_crypto_list.append([crypto.name, crypto])

    user_crypto_objects_list = []

    for crypto_name, crypto in user_crypto_list:
        owned_coins = 0

        if user_purchases:
            for purchase in user_purchases:
                if crypto_name == purchase.currency:
                    owned_coins += purchase.quantity

        if user_trades:
            for trade in user_trades:
                if crypto_name == trade.traded_currency_one:
                    owned_coins += trade.converted_from_quantity
                elif crypto_name == trade.traded_currency_two:
                    owned_coins += trade.converted_to_quantity

        if user_sales:
            for sale in user_sales:
                if crypto_name == sale.currency:
                    if sale.seller.pk == user_pk:
                        owned_coins -= sale.quantity
                    elif sale.buyer.pk == user_pk:
                        owned_coins += sale.quantity

        user_crypto_objects_list.append([crypto, owned_coins])

    return user_crypto_objects_list
