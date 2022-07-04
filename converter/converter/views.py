from django.shortcuts import render

from .forms import ExchangeForm
from . import services


def converter(request):
    currencies_values = services.get_currencies_values()
    currencies_list = currencies_values.keys()

    if request.method == 'POST':
        form = ExchangeForm(request.POST, currencies=currencies_list)
        if form.is_valid():
            form_data = form.cleaned_data
            converted_amount = services.convert(form_data['amount'],
                                                form_data['from_currency'],
                                                form_data['to_currency'],
                                                currencies_values)
            context = {
                'form': form,
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
