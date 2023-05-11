from django import forms
from CryptoTradingApp.crypto.models import CryptoCurrency
from CryptoTradingApp.core.mixins import DisabledFormMixin, HiddenFieldsMixin


class CryptoBaseForm(forms.ModelForm):
    class Meta:
        model = CryptoCurrency
        fields = ("name", "photo", "price", "quantity", "description")

        labels = {
            "price": "Price is in USD",
            "quantity": "Quantity in Coins"
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Crypto Name"
                }
            ),
            # "photo": forms.
            "price": forms.TextInput(
                attrs={
                    "placeholder": "Price $$$"
                },
            ),
            "quantity": forms.TextInput(
                attrs={
                    "placeholder": "How many Coins"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Write something..."
                }
            )
        }


class CryptoCreateForm(CryptoBaseForm):
    pass


class CryptoEditForm(DisabledFormMixin, CryptoBaseForm):
    disabled_fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields()


class CryptoDeleteForm(HiddenFieldsMixin, CryptoBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_hidden_fields()

    def save(self, commit=True):
        if commit:
            self.instance.delete()

        return self.instance
