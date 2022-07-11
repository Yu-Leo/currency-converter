import datetime
import functools
import logging

from django.core.exceptions import ValidationError
from django.shortcuts import render

from . import services
from .forms import ExchangeForm

logger = logging.getLogger('main')


def base_view(func):
    @functools.wraps(func)
    def inner(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as e:
            logger.critical(str(e))
            return render(request, 'converter/error_page.html', {})

    return inner


@base_view
def converter(request):
    currencies_list = services.get_currencies_list()
    if request.method == 'POST':
        form = ExchangeForm(request.POST, currencies=currencies_list)
        try:
            operation = form.get_operation()
        except ValidationError:
            return render(request, 'converter/index.html', {'form': form, })
        converted_amount = services.convert(operation)
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
