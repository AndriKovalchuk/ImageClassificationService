from django.shortcuts import render


def index(request):
    return render(request, 'InfinityVision/index.html')


def about(request):
    return render(request, 'InfinityVision/about.html')


def facts(request):
    return render(request, 'InfinityVision/facts.html')


def contact(request):
    return render(request, 'InfinityVision/contact.html')
