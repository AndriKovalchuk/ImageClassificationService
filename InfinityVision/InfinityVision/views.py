from django.shortcuts import render


def index(request):
    return render(request, 'InfinityVision/index.html')


def about(request):
    return render(request, 'InfinityVision/about.html')
