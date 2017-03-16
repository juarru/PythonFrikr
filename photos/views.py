# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from photos.forms import PhotoForm
from photos.models import Photo, PUBLIC
from django.contrib.auth.decorators import login_required


def home(request):
    photos = Photo.objects.filter(visibility=PUBLIC).order_by('-created_at')
    """
    Esta función devuelve el home de la página
    """
    context = {
        'photos_list': photos[:5]
    }

    return render(request, 'photos/home.html', context)


def detail(request, pk):
    """
    Carga la página de detalle de una foto
    :param request: HttpRequest
    :param pk: id de la photo
    :return: HttpResponse
    """

    possible_photos = Photo.objects.filter(pk=pk)

    # Controlo que en la lista sólo recibo un valor. Si recibo mas de uno devuelve None
    photo = possible_photos[0] if len(possible_photos) == 1 else None

    if  photo is not None:
        # Cargamos la plantilla de detalle
        context = {
            'photo': photo
        }

        return render(request, 'photos/detail.html', context)

    else:
        return HttpResponseNotFound('No existe la foto') # 404 not found


@login_required()
def create(request):

    """
    Muestra un formulario para crear una foto y la crea si la petición es POST
    :param request: HttpRequest
    :return: HttpResponse
    """

    success_message = ''

    if request.method == 'GET':
        form = PhotoForm()
    else:
        photo_with_owner = Photo()
        photo_with_owner.owner = request.user #asigno com propietario de la foto al usuario autenticado
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
            new_photo = form.save() # Guarda el objeto y lo devuelve
            form = PhotoForm()
            success_message = 'Guardado con exito'
            success_message += '<a href="{0}">'.format(reverse('photo_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'

    context = {
        'form': form,
        'success_message': success_message
    }
    return render(request, 'photos/new_photo.html', context)