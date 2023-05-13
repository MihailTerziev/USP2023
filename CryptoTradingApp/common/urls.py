from django.urls import path
from CryptoTradingApp.common.views import *


urlpatterns = (
    path("", index_page, name="index-page"),
    path("catalogue/", catalogue_page, name="catalogue-page"),
    path("trade/", trade_page, name="trade-page"),
    path("purchase/", purchase_page, name="purchase-page"),
    path("sell/", sale_page, name="sale-page"),
    path("login/", SignInView.as_view(), name="login-user-page"),
    path("register/", SignUpView.as_view(), name="register-user-page"),
    path("logout/", SignOutView.as_view(), name="logout-page")
)

from CryptoTradingApp.core.signals import *
