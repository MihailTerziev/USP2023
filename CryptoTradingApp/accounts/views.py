from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views import generic as views
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.contrib.auth.decorators import login_required
from CryptoTradingApp.accounts.forms import *
from CryptoTradingApp.crypto.models import *
from CryptoTradingApp.common.forms import *
from CryptoTradingApp.core.utils import get_user_crypto_objects_list


UserModel = get_user_model()


class UserEditView(views.UpdateView):
    template_name = "users/edit-user-profile-page.html"
    model = UserModel
    fields = ("first_name", "last_name", "photo", "date_of_birth", "email", "phone_number")

    def get_success_url(self):
        return reverse_lazy(
            "details-user-page",
            kwargs={
                "pk": self.request.user.pk
            }
        )


class UserDeleteView(views.DeleteView):
    template_name = "users/delete-user-profile-page.html"
    model = UserModel
    success_url = reverse_lazy("index-page")


class UserDetailsView(views.DetailView):
    template_name = "users/details-user-profile-page.html"
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = CryptoWallet.objects.filter(pk=self.object.pk).get()

        # request user is the logged-in user and object is the selected user by pk form db
        context["is_owner"] = self.request.user == self.object
        context["wallet_balance"] = wallet.balance

        return context


@login_required(login_url='/login/')
def trade_page(request):
    if request.method == 'GET':
        form = TradeCreateForm
    else:
        form = TradeCreateForm(request.POST)

        if form.is_valid():
            form.create_trade(request.user)
            return redirect('wallet-page')

    context = {
        'form': form
    }

    return render(request, "users/trade-page.html", context)


def purchase_page(request):  # TODO Implement error display
    if request.method == 'GET':
        form = PurchaseCreateForm()
    else:
        form = PurchaseCreateForm(request.POST)

        if form.is_valid():
            form.create_purchase(request.user)
            return redirect('wallet-page')

    context = {
        'form': form
    }

    return render(request, "users/purchase-page.html", context)


def sale_page(request):
    if request.method == 'GET':
        form = SaleCreateForm()
    else:
        form = SaleCreateForm(request.POST)

        if form.is_valid():
            form.create_sale(request.user)
            return redirect('wallet-page')

    context = {
        'form': form
    }

    return render(request, "users/sale-page.html", context)


def increase_balance_page(request):
    wallet = CryptoWallet.objects.filter(pk=request.user.pk).get()

    if request.method == 'GET':
        form = IncreaseBalanceForm()
    else:
        form = IncreaseBalanceForm(request.POST)

        if form.is_valid():
            add_amount = form.cleaned_data['amount']

            wallet.balance += float(add_amount)
            wallet.save()

            BalanceIncrease.objects.create(
                amount=add_amount,
                transaction_method=form.cleaned_data['transaction_method'],
                user=request.user,
            )

            return redirect("wallet-page")

    context = {
        "form": form
    }

    return render(request, "users/increase-balance-page.html", context)


def catalogue_page(request):
    context = {
        "crypto": CryptoCurrency.objects.all()
    }

    return render(request, "common/catalog-page.html", context)


def search_page(request):  # TODO Implement search page
    return render(request, "common/search-page.html")


def wallet_page(request):  # TODO find a way to calculate how many crypto a user owns
    user_purchases = CryptoPurchase.objects.filter(buyer_id=request.user.pk)
    user_trades = CryptoTrade.objects.filter(trader_id=request.user.pk)
    user_sales = CryptoSale.objects.all()
    user_crypto = get_user_crypto_objects_list(request.user.pk, user_purchases, user_trades, user_sales)
    wallet = CryptoWallet.objects.filter(pk=request.user.pk).get()

    context = {
        "crypto": user_crypto,
        "current_balance": wallet.balance,
    }

    return render(request, "users/wallet-page.html", context)


# TODO Implement staff functionality and views
def create_admin_user_page(request):
    if request.method == 'GET':
        form = SuperuserCreateForm()
    else:
        form = SuperuserCreateForm(request.POST)

        if form.is_valid():
            UserModel.objects.create_superuser(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                date_of_birth=form.cleaned_data["date_of_birth"],
                email=form.cleaned_data["email"],
                phone_number=form.cleaned_data["phone_number"],
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"]
            )
            return redirect("index-page")

    context = {
        "form": form
    }

    return render(request, "users/admins/create-admin-page.html", context)


def staff_list_page(request):  # TODO Implement staff list page
    return render(request, "users/admins/staff-list-page.html")


def users_list_page(request):  # TODO Implement users list page
    return render(request, "users/admins/users-list-page.html")
