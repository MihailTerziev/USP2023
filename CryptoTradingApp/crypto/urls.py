from django.urls import path, include
from CryptoTradingApp.crypto.views import *

'''
Crypto Add Page: http://127.0.0.1:8000/crypto/add/
Crypto Details Page: http://127.0.0.1:8000/crypto/<slug:crypto_slug>/details/
Crypto Edit Page: http://127.0.0.1:8000/crypto/<slug:crypto_slug>/edit/
Crypto Delete Page: http://127.0.0.1:8000/crypto/<slug:crypto_slug>/delete/
'''

urlpatterns = (
    path("add/", add_crypto_page, name="add-crypto-page"),
    path("<slug:crypto_slug>/", include([
        path("details/", details_crypto_page, name="details-crypto-page"),
        path("edit/", edit_crypto_page, name="edit-crypto-page"),
        path("delete/", delete_crypto_page, name="delete-crypto-page")
    ]))
)
