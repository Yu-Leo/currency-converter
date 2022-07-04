from django.shortcuts import render

from .forms import ExchangeForm


def converter(request):
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
    else:
        form = ExchangeForm()
    context = {"form": form}
    return render(request, 'converter/index.html', context)
