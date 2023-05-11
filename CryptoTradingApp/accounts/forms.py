from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from CryptoTradingApp.crypto.models import CryptoWallet


UserModel = get_user_model()


class UserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("username", "email")

        field_classes = {
            "username": auth_forms.UsernameField
        }


class UserEditForm(auth_forms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = "__all__"
        field_classes = {
            "username": auth_forms.UsernameField
        }

        widgets = {
            "photo": forms.ImageField(),
            "date_of_birth": forms.DateInput()
        }


class SuperuserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("first_name", "last_name", "username", "email", "date_of_birth", "phone_number", "password1", "password2")

        field_classes = {
            "username": auth_forms.UsernameField
        }

# TODO Implement more forms
