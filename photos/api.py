# -*- coding: utf-8 -*-
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from photos.models import Photo
from photos.serializers import PhotoSerializer, PhotoListSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from photos.views import PhotosQuerySet


class PhotoViewSet(PhotosQuerySet, ModelViewSet):
    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description', 'owner__first_name')
    ordering_fields = ('name', 'owner')

    def get_queryset(self):
        return self.get_photos_queryset(self.request)

    def get_serializer_class(self):
        if self.action == 'list':
            return PhotoListSerializer
        else:
            return PhotoSerializer

    def perform_create(self, serializer):
        """
        Asigna automáticamente la autoria de la nueva foto al usuario autenticado
        :param serializer:
        :return:
        """
        serializer.save(owner=self.request.user)