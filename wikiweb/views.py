from django.shortcuts import render
from django.conf import settings


def index(request, path=''):
    context = {
        'DEVMODE': settings.DEVMODE
    }

    return render(request, 'wikiweb/index.html', context)
