from django.shortcuts import render

from .forms import ExchangeForm
from . import services
from . import exceptions

def converter(request):
    try:
        currencies_values = services.get_currencies_values()
    except exceptions.APIException:
        return render(request, 'converter/error_page.html', {})

    currencies_list = currencies_values.keys()

    if request.method == 'POST':
        form = ExchangeForm(request.POST, currencies=currencies_list)
        if form.is_valid():
            form_data = form.cleaned_data
            amount = round(form_data['amount'], 2)
            from_currency = form_data['from_currency']
            to_currency = form_data['to_currency']
            converted_amount = services.convert(amount,
                                                from_currency,
                                                to_currency,
                                                currencies_values)
            context = {
                'form': form,
                'amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'converted_amount': converted_amount,
            }
        else:
            context = {
                'form': form,
            }
    else:
        form = ExchangeForm(currencies=currencies_list)
        context = {
            'form': form,
        }

    return render(request, 'converter/index.html', context)
