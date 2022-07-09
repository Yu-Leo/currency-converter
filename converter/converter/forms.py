from django import forms
from django.core.exceptions import ValidationError

from .services import Operation


class ExchangeForm(forms.Form):
    amount = forms.FloatField()
    from_currency = forms.ChoiceField()
    to_currency = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        currencies_list = kwargs.pop('currencies')
        self.currencies = tuple(zip(currencies_list, currencies_list))
        super(ExchangeForm, self).__init__(*args, **kwargs)
        self.fields['to_currency'].choices = self.currencies
        self.fields['from_currency'].choices = self.currencies

    def get_operation(self) -> Operation:
        if not self.is_valid():
            raise ValidationError

        form_data = self.cleaned_data
        amount = round(form_data['amount'], 2)
        from_currency = form_data['from_currency']
        to_currency = form_data['to_currency']
        return Operation(amount, from_currency, to_currency)
