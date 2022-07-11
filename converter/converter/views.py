import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render

from . import services
from .forms import ExchangeForm


def converter(request):
    try:
        currencies_list = services.get_currencies_list()
    except services.exceptions.GettingDataError:
        return render(request, 'converter/error_page.html', {})

    if request.method == 'POST':
        form = ExchangeForm(request.POST, currencies=currencies_list)
        try:
            operation = form.get_operation()
        except ValidationError:
            context = {
                'form': form,
            }
            return render(request, 'converter/index.html', context)

        try:
            converted_amount = services.convert(operation)
        except services.exceptions.ConversionError:
            return render(request, 'converter/error_page.html', {})

        context = {
            'form': form,
            'amount': operation.amount,
            'primary_currency': operation.primary_currency,
            'secondary_currency': operation.secondary_currency,
            'converted': True,
            'converted_amount': converted_amount,
            'date': datetime.date.today(),
        }

    else:
        form = ExchangeForm(currencies=currencies_list)
        context = {
            'form': form,
        }

    return render(request, 'converter/index.html', context)
