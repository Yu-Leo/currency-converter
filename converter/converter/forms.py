from django import forms


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
