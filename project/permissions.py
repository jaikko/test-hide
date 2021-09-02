from django.http import request
from rest_framework import permissions, views
from .models import *


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):

        if Staff.objects.get(pk=request.user.id):
            if request.method in permissions.SAFE_METHODS:
                return True
            return False
        return False


class IsSaleTeam(permissions.BasePermission):
    def has_permission(self, request, view):

        if Staff.objects.filter(id=request.user.id, team="Sale").exists():
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.sale_contact == request.user


class IsSupportTeam(permissions.BasePermission):
    def has_permission(self, request, view):

        if Staff.objects.filter(id=request.user.id, team="Support").exists():
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                if request.method == 'POST':
                    return False
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.support_contact == request.user


class EventAcces(permissions.BasePermission):
    def has_permission(self, request, view):

        if Staff.objects.filter(id=request.user.id, team="Management").exists():
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                if request.method == 'POST':
                    return False
            return True

        if Staff.objects.filter(id=request.user.id, team="Sale").exists():
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                if request.method == 'POST':
                    id = request.resolver_match.kwargs.get('contract_pk')
                    return Contract.objects.filter(id=id, sale_contact=request.user.id).exists()
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if Staff.objects.filter(id=request.user.id, team="Management"):
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.client.sale_contact == request.user
