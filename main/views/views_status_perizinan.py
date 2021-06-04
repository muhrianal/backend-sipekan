from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate

from ..models.profile import Profile
from django.contrib.auth.models import User


from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from ..permissions import AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM

from ..models.peminjaman_ruangan import PeminjamanRuangan

from ..models.peminjaman_ruangan import Ruangan

from ..models.izin_kegiatan import IzinKegiatan

from ..serializers.peminjaman_ruangan_serializer import PeminjamanRuanganSerializer, RuanganSerializer

from..serializers.izin_kegiatan_serializer import IzinKegiatanSerializer, DetailKegiatanSerializer, IzinKegiatanSerializerDetailed
from django.http.response import JsonResponse

@api_view(['GET'])
@permission_classes([permissions.AllowAny,])
def list_perizinan(request):
    if request.method == 'GET':
        list_izin_kegiatan = IzinKegiatan.objects.all()
        izin_kegiatan_serialized = IzinKegiatanSerializer(list_izin_kegiatan, many=True)
        return JsonResponse(izin_kegiatan_serialized.data, safe=False)

    #case for else
    data = {
        'message' : 'invalid API call'
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.AllowAny,])
def detail_perizinan(request,pk):
    try:
        perizinan = IzinKegiatan.objects.get(pk=pk)
    except IzinKegiatan.DoesNotExist:
        return JsonResponse({'message': 'Izin kegiatan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        perizinan_serialized = IzinKegiatanSerializer(perizinan)
        return JsonResponse(perizinan_serialized.data, safe=False)
    data = {
            'message' : 'invalid API call'
        }
    # elif request.method == 'PUT':
    #         perizinan_data = JSONParser().parse(request)
    #         perizinan_serializer = IzinKegiatanSerializer(perizinan, data=perizinan_data)
    #         if perizinan_serializer.is_valid():
    #             perizinan_serializer.save()
    #             return JsonResponse(perizinan_serializer.data)
    #         return JsonResponse(perizinan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowOnlyAdminFASTUR|AllowOnlyAdminHUMAS|AllowOnlyAdminPKM])
def list_perizinan_detailed(request):
    if request.method == 'GET':
        list_izin_kegiatan = IzinKegiatan.objects.all()
        izin_kegiatan_serialized = IzinKegiatanSerializerDetailed(list_izin_kegiatan, many=True)
        return JsonResponse(izin_kegiatan_serialized.data, safe=False)

    #case for else
    data = {
        'message' : 'invalid API call'
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
