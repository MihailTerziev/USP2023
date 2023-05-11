from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("CryptoTradingApp.common.urls")),
    path("crypto/", include("CryptoTradingApp.crypto.urls")),
    path("accounts/", include("CryptoTradingApp.accounts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
