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

from ..models.humas import PerizinanPublikasi, PermintaanProtokoler, PermintaanSouvenir, JenisPublikasi, Souvenir

from ..models.izin_kegiatan import IzinKegiatan

from ..serializers.humas_serializer import PermintaanSouvenirSeriliazer,PerizinanPublikasiSerializer,PermintaanProtokolerSerializer, PerizinanKegiatanSerializer, JenisPublikasiSerializer,SouvenirSerializer,PerizinanPublikasiSerializer

from django.http.response import JsonResponse
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET'])
@permission_classes([permissions.AllowAny,])
def list_perizinan_humas(request):

    if request.method == 'GET':
        list_perizinan_humas_kegiatan = IzinKegiatan.objects.all()
        list_perizinan_humas_kegiatan_serialized = PerizinanKegiatanSerializer(list_perizinan_humas_kegiatan,many=True)
        return JsonResponse(list_perizinan_humas_kegiatan_serialized.data, safe=False)
    
    #case for else
    data = {
        'message' : 'invalid API call'
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny,])
def get_post_perizinan_humas(request,id_izin_kegiatan):
    try: 
        izin_kegiatan =IzinKegiatan.objects.get(pk=id_izin_kegiatan)
    except:
        return JsonResponse({'message': 'Izin kegiatan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        permintaan_data = JSONParser().parse(request)
        permintaan_humas_serialized = PerizinanKegiatanSerializer(izin_kegiatan, data = permintaan_data)
        if permintaan_humas_serialized.is_valid():
            permintaan_humas_serialized.save()
            return JsonResponse(permintaan_humas_serialized.data,safe=False)
        return JsonResponse(permintaan_humas_serialized.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        detail_perizinan_humas_kegiatan_serialized = PerizinanKegiatanSerializer(izin_kegiatan)
        return JsonResponse(detail_perizinan_humas_kegiatan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny,]) 
@parser_classes([MultiPartParser, FormParser])
def post_perizinan_publikasi(request):
    if request.method == 'POST': # post detail izin kegiatan
        perizinan_data_serialized = PerizinanPublikasiSerializer(data=request.data)
        if perizinan_data_serialized.is_valid():
            perizinan_data_serialized.save()
            return JsonResponse(perizinan_data_serialized.data,status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(perizinan_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny,]) #nanti diganti jadi mahasiswa dan unit kerja
def get_jenis_publikasi(request):
    if request.method == 'GET':
        list_jenis_publikasi = JenisPublikasi.objects.all()
        list_jenis_publikasi_serialized = JenisPublikasiSerializer(list_jenis_publikasi, many=True)
        return JsonResponse(list_jenis_publikasi_serialized.data,safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([permissions.AllowAny,]) #nanti diganti jadi mahasiswa dan unit kerja
def get_list_souvenir(request):
    if request.method == 'GET':
        list_souvenir = Souvenir.objects.all()
        list_souvenir_serialized = SouvenirSerializer(list_souvenir, many=True)
        return JsonResponse(list_souvenir_serialized.data,safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

