from rest_framework import permissions
from .models.profile import Profile


MAHASISWA = 'MAHASISWA'
ADMIN_PKM = 'ADMIN PKM'
ADMIN_FASTUR = 'ADMIN FASTUR'
ADMIN_HUMAS =  'ADMIN HUMAS'
UNIT_KERJA =  'UNIT KERJA'

class AllowOnlyAdminPKM(permissions.BasePermission):
    def has_permission(self, request, view):
        return Profile.objects.get(user=request.user).role == ADMIN_PKM

class AllowOnlyAdminFASTUR(permissions.BasePermission):
    def has_permission(self, request, view):
        return Profile.objects.get(user=request.user).role == ADMIN_FASTUR

class AllowOnlyAdminHUMAS(permissions.BasePermission):
    def has_permission(self, request, view):
        return Profile.objects.get(user=request.user).role == ADMIN_HUMAS

class AllowOnlyUnitKerja(permissions.BasePermission):
    def has_permission(self, request, view):
        return Profile.objects.get(user=request.user).role == UNIT_KERJA

class AllowOnlyMahasiswa(permissions.BasePermission):
    def has_permission(self, request, view):
        return Profile.objects.get(user=request.user).role == MAHASISWA