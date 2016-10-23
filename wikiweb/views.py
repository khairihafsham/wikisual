from django.shortcuts import render


def index(request, path=''):
    return render(request, 'wikiweb/index.html')
