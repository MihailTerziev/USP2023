from django.shortcuts import render, redirect
from CryptoTradingApp.crypto.models import CryptoCurrency
from CryptoTradingApp.crypto.forms import *


def add_crypto_page(request):
    if request.method == "GET":
        form = CryptoCreateForm()
    else:
        form = CryptoCreateForm(request.POST, request.FILES)

        if form.is_valid():
            crypto = form.save(commit=False)
            crypto.creator = request.user
            crypto.save()
            return redirect("index-page")

    context = {
        "form": form
    }

    return render(request, "crypto/add-crypto-page.html", context)


def edit_crypto_page(request, crypto_slug):
    crypto_currency = CryptoCurrency.objects.filter(slug=crypto_slug).get()

    if request.method == "GET":
        form = CryptoEditForm(instance=crypto_currency)
    else:
        form = CryptoEditForm(request.POST, request.FILES, instance=crypto_currency)

        if form.is_valid():
            form.save()
            return redirect("details-crypto-page", crypto_slug=crypto_slug)

    context = {
        "form": form,
        "crypto_slug": crypto_slug
    }

    return render(request, "crypto/edit-crypto-page.html", context)


def delete_crypto_page(request, crypto_slug):
    crypto_currency = CryptoCurrency.objects.filter(slug=crypto_slug).get()

    if request.method == "GET":
        form = CryptoDeleteForm(instance=crypto_currency)
    else:
        form = CryptoDeleteForm(request.POST, instance=crypto_currency)

        if form.is_valid():
            form.save()
            return redirect("catalogue-page")

    context = {
        "form": form,
        "crypto_slug": crypto_slug
    }

    return render(request, "crypto/delete-crypto-page.html", context)


def details_crypto_page(request, crypto_slug):
    crypto_currency = CryptoCurrency.objects.filter(slug=crypto_slug).get()

    context = {
        "crypto": crypto_currency
    }

    return render(request, "crypto/details-crypto-page.html", context)
