from django.urls import path, include
from CryptoTradingApp.crypto.views import *


urlpatterns = (
    path("add/", add_crypto_page, name="add-crypto-page"),
    path("<slug:crypto_slug>/", include([
        path("details/", details_crypto_page, name="details-crypto-page"),
        path("edit/", edit_crypto_page, name="edit-crypto-page"),
        path("delete/", delete_crypto_page, name="delete-crypto-page")
    ]))
)
