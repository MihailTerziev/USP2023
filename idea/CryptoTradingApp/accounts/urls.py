from django.urls import path, include
from CryptoTradingApp.accounts.views import *


urlpatterns = (
    path("balance/", increase_balance_page, name="increase-balance-page"),
    path("wallet/", wallet_page, name="wallet-page"),
    path("profile/<int:pk>/", include([
        path("details", UserDetailsView.as_view(), name="details-user-page"),
        path("edit/", UserEditView.as_view(), name="edit-user-page"),
        path("delete/", UserDeleteView.as_view(), name="delete-user-page")
    ])),
    path("superusers/", include([
        path("create/", create_admin_user_page, name="create-admin-page"),
        path("staff/create", create_staff_user_page, name="create-staff-page"),
    ]))
)

from CryptoTradingApp.core.signals import *
