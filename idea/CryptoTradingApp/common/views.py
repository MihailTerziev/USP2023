from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, get_user_model, login
from django.views import generic as views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from CryptoTradingApp.accounts.forms import UserCreateForm
from CryptoTradingApp.crypto.models import *
from CryptoTradingApp.common.forms import *


UserModel = get_user_model()


def index_page(request):
    return render(request, "common/index-home-page.html")


def catalogue_page(request):
    crypto = CryptoCurrency.objects.all()

    search_form = SearchCryptoForm(request.GET)
    searched_name = None

    if search_form.is_valid():
        searched_name = search_form.cleaned_data["search_crypto_currencies_by_name"]

    if searched_name:
        crypto = crypto.filter(name__icontains=searched_name)

    context = {
        "crypto": crypto,
        "search_form": search_form
    }

    return render(request, "common/catalog-page.html", context)


@login_required(login_url='/login/')
def trade_page(request):
    potential_error = None

    if request.method == "GET":
        form = TradeCreateForm()
    else:
        form = TradeCreateForm(request.POST)

        if form.is_valid():
            potential_error = form.create_trade(request)

            if potential_error is None:
                return redirect('wallet-page')

    context = {
        'form': form,
        'error': potential_error
    }

    return render(request, "common/trade-page.html", context)


def purchase_page(request):
    potential_error = None

    if request.method == "GET":
        form = PurchaseCreateForm()
    else:
        form = PurchaseCreateForm(request.POST)

        if form.is_valid():
            potential_error = form.create_purchase(request)

            if potential_error is None:
                return redirect('wallet-page')

    context = {
        'form': form,
        'error': potential_error
    }

    return render(request, "common/purchase-page.html", context)


def sale_page(request):
    potential_error = None

    if request.method == "GET":
        form = SaleCreateForm()
    else:
        form = SaleCreateForm(request.POST)

        if form.is_valid():
            potential_error = form.create_sale(request)

            if potential_error is None:
                return redirect('wallet-page')

    context = {
        'form': form,
        'error': potential_error
    }

    return render(request, "common/sale-page.html", context)


class SignInView(auth_views.LoginView):
    template_name = "common/login-page.html"


class SignUpView(views.CreateView):
    template_name = "common/register-page.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("index-page")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login(request, self.object)
        return response


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy("index-page")
