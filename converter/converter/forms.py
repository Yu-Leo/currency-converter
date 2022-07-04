from django import forms


class ExchangeForm(forms.Form):
    amount = forms.IntegerField()
    from_currency = forms.Select()
    to_currency = forms.Select()
