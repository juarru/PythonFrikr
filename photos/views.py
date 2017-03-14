#-*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from photos.models import Photo


def home(request):


    photos = Photo.objects.all().order_by('-created_at')
    """
    Esta función devuelve el home de la página
    """
    context = {
        'photos_list': photos[:5]
    }

    return render(request, 'photos/home.html', context)
