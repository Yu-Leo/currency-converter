from django import forms
from django.core.exceptions import ValidationError

from .services import Operation


class ExchangeForm(forms.Form):
    amount = forms.FloatField()
    primary_currency = forms.ChoiceField()
    secondary_currency = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        currencies_list = kwargs.pop('currencies')
        self.currencies = tuple(zip(currencies_list, currencies_list))
        super(ExchangeForm, self).__init__(*args, **kwargs)
        self.fields['secondary_currency'].choices = self.currencies
        self.fields['primary_currency'].choices = self.currencies

    def get_operation(self) -> Operation:
        if not self.is_valid():
            raise ValidationError

        form_data = self.cleaned_data
        amount = round(form_data['amount'], 2)
        primary_currency = form_data['primary_currency']
        secondary_currency = form_data['secondary_currency']
        return Operation(amount, primary_currency, secondary_currency)
