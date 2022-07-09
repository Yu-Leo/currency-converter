from django.core.exceptions import ValidationError
from django.shortcuts import render

from . import exceptions
from . import services
from .forms import ExchangeForm


def converter(request):
    try:
        currencies_list = services.get_currencies_list()
    except exceptions.APIException:
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
            currencies_values = services.get_currencies_values()
        except exceptions.APIException:
            return render(request, 'converter/error_page.html', {})

        try:
            converted_amount = services.convert(operation.amount,
                                                operation.from_currency,
                                                operation.to_currency,
                                                currencies_values)
        except exceptions.ExchangeRateException:
            return render(request, 'converter/error_page.html', {})

        context = {
            'form': form,
            'amount': operation.amount,
            'from_currency': operation.from_currency,
            'to_currency': operation.to_currency,
            'converted': True,
            'converted_amount': converted_amount,
        }

    else:
        form = ExchangeForm(currencies=currencies_list)
        context = {
            'form': form,
        }

    return render(request, 'converter/index.html', context)
