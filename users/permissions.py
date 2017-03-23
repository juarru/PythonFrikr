# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request tiene permiso para realizar acciones
        :param request:
        :param view:
        :return: Boolean
        """
        # Si quiere crear un usuario, sea quien sea puede
        #from users.api import UserDetailAPI
        if view.action == 'create':
            return True
        # Si no es POST, el superusuario siempre puede
        elif request.user.is_superuser:
            return True
        # Si es un GET a la vista de detalle, tomo la decisión en has_object_permissions
        elif view.action in ['retrieve', 'update', 'destroy']:
            return True
        else:
            # GET a /api/1.0/users/
            return False

    def has_object_permission(self, request, view, obj):
        """
        Define para que acciones tiene permisos el usuario autenticado sobre el objeto obj
        :param request:
        :param view:
        :param obj:
        :return:
        """
        # Si es superadmin, o el usuario autenticado intenta
        # hacer GET, PUT o DELETE sobre su mismo perfil

        return request.user.is_superuser or request.user == obj