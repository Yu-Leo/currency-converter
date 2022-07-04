from django.shortcuts import render

from .forms import ExchangeForm
from . import services


def converter(request):
    currencies_values = services.get_currencies_values()
    currencies_list = currencies_values.keys()

    if request.method == 'POST':
        form = ExchangeForm(request.POST, currencies=currencies_list)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = ExchangeForm(currencies=currencies_list)
    context = {"form": form}
    return render(request, 'converter/index.html', context)
