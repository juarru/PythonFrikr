from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


class UserListAPI(APIView):

    def get(self, request):
        # Instancio paginador
        paginator = PageNumberPagination()

        users = User.objects.all()
        # paginamos el queryset
        paginator.paginate_queryset(users, request)
        serializer = UserSerializer(users, many=True)

        serialized_users = serializer.data # lista de diccionarios
        # Devolvemos respuesta paginada
        return paginator.get_paginated_response(serialized_users)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDetailAPI(APIView):

    def get(self, request, pk):

        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serialiazer = UserSerializer(instance=user, data=request.data)
        if serialiazer.is_valid():
            serialiazer.save()
            return Response(serialiazer.data, status=status.HTTP_200_OK)
        else:
            return Response(serialiazer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)