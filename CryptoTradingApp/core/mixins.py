from django import forms


class GetUserNamesMixin:
    @staticmethod
    def names(obj):
        return f"{obj.first_name} {obj.last_name}"


class GetBuyerNamesMixin:
    @staticmethod
    def names(obj):
        return f"{obj.buyer.first_name} {obj.buyer.last_name}"


class DisabledFormMixin:
    disabled_fields = ()
    fields = {}

    def _disable_fields(self):
        if self.disabled_fields == '__all__':
            fields = self.fields.keys()
        else:
            fields = self.disabled_fields

        for field_name in fields:
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs['disabled'] = 'disabled'
                field.widget.attrs['readonly'] = 'readonly'


class HiddenFieldsMixin:
    def _set_hidden_fields(self):
        for _, field in self.fields.items():
            field.widget = forms.HiddenInput()


class ReadOnlyFieldsMixin:
    readonly_fields = ()
    fields = {}

    def _set_readonly_fields(self):
        if self.readonly_fields == '__all__':
            fields = self.fields.keys()
        else:
            fields = self.readonly_fields

        for field_name in fields:
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs['readonly'] = 'readonly'


class DeleteFormMixin:
    def save(self, commit=True):
        if commit:
            self.instance.delete()

        return self.instance


class ChoicesEnumMixin:
    @classmethod
    def choices(cls, add_wallet_balance=False):
        choices_list = []

        if add_wallet_balance:
            choices_list = [("wallet_balance", "Crypto wallet balance")]

        choices_list.extend([(x.name, x.value) for x in cls])
        return choices_list

    @classmethod
    def max_len(cls):
        return max(len(name) for name, _ in cls.choices())
