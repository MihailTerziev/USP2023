from django.urls import path, include
from CryptoTradingApp.accounts.views import *

'''
Trade Page: http://127.0.0.1:8000/accounts/trade/
Purchase Page: http://127.0.0.1:8000/accounts/purchase/
Catalogue Page: http://127.0.0.1:8000/accounts/catalogue/
Search Page: http://127.0.0.1:8000/accounts/search/
Wallet Page: http://127.0.0.1:8000/accounts/wallet/
Profile Details Page: http://127.0.0.1:8000/accounts/profile/<int:pk>/details
Profile Edit Page: http://127.0.0.1:8000/accounts/profile/<int:pk>/edit/
Profile Delete Page: http://127.0.0.1:8000/accounts/profile/<int:pk>/delete/
'''

urlpatterns = (
    path("trade/", trade_page, name="trade-page"),
    path("purchase/", purchase_page, name="purchase-page"),
    path("sell/", sale_page, name="sale-page"),
    path("balance/", increase_balance_page, name="increase-balance-page"),
    path("search/", search_page, name="search-page"),
    path("wallet/", wallet_page, name="wallet-page"),
    path("catalogue/", catalogue_page, name="catalogue-page"),
    path("profile/<int:pk>/", include([
        path("details", UserDetailsView.as_view(), name="details-user-page"),
        path("edit/", UserEditView.as_view(), name="edit-user-page"),
        path("delete/", UserDeleteView.as_view(), name="delete-user-page")
    ])),
    path("superusers/", include([
        path("create/", create_admin_user_page, name="create-admin-page"),
        path("staff/", staff_list_page, name="staff-list-page"),
        path("users/", users_list_page, name="users-list-page")
    ]))
)

from CryptoTradingApp.core.signals import *
