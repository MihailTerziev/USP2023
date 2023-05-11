from django.urls import path
from CryptoTradingApp.common.views import *

'''
Home Page: http://127.0.0.1:8000/
Login Page: http://127.0.0.1:8000/login/
Login Admin Page: http://127.0.0.1:8000/login/admin/
Register Page: http://127.0.0.1:8000/register/
Logout Page: http://127.0.0.1:8000/logout/
'''

urlpatterns = (
    path("", index_page, name="index-page"),
    path("login/", SignInView.as_view(), name="login-user-page"),
    path("register/", SignUpView.as_view(), name="register-user-page"),
    path("logout/", SignOutView.as_view(), name="logout-page")
)

from CryptoTradingApp.core.signals import *
