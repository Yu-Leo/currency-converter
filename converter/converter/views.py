from django.shortcuts import render

def converter(request):
    context = {}
    return render(request, 'converter/index.html', context)