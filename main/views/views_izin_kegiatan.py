from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate

from django.utils import timezone
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

from ..models.izin_kegiatan import DetailKegiatan, IzinKegiatan

from ..models.humas import PermintaanSouvenir, PermintaanProtokoler, JenisIzinPublikasi, Souvenir

from ..serializers.humas_serializer import SouvenirSerializerSimpliest

from ..serializers.izin_kegiatan_serializer import IzinKegiatanSerializerSimplified, DetailKegiatanSerializer, IzinKegiatanMahasiswaSerializer, IzinKegiatanSimpliest, IzinKegiatanMahasiswaSerializer1


from django.http.response import JsonResponse


@api_view(['PUT',])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])
def update_izin_kegiatan_by_id_perizinan(request, id_perizinan):
    try:
        izin_kegiatan = IzinKegiatan.objects.get(pk=id_perizinan)
    except:
        return JsonResponse({'message': 'Izin kegiatan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        izin_data = JSONParser().parse(request) 
        try:
            izin_kegiatan.status_perizinan_kegiatan = izin_data["status_perizinan_kegiatan"]
            izin_kegiatan.detail_kegiatan.updated_at = izin_data["detail_kegiatan"]["updated_at"]
            if izin_data["detail_kegiatan"]["alasan_penolakan"] is not None:
                izin_kegiatan.detail_kegiatan.alasan_penolakan = izin_data["detail_kegiatan"]["alasan_penolakan"] 
            izin_kegiatan.detail_kegiatan.save()
            izin_kegiatan.save()
            izin_kegiatan_serialized = IzinKegiatanMahasiswaSerializer1(data=izin_kegiatan)
            if izin_kegiatan_serialized.is_valid():
                izin_kegiatan_serialized.save()
            return JsonResponse(izin_kegiatan_serialized.data, safe=False)
        except:
           return JsonResponse(izin_kegiatan.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 

@api_view(['POST','GET'])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])
def list_izin_kegiatan(request):

    if request.method == 'POST':
        izin_data = JSONParser().parse(request)
        izin_kegiatan_serialized = IzinKegiatanMahasiswaSerializer(data=izin_data)
        if izin_kegiatan_serialized.is_valid():
            izin_kegiatan_serialized.save()
            return JsonResponse( izin_kegiatan_serialized.data, status=status.HTTP_201_CREATED) 
        return JsonResponse( izin_kegiatan_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        list_izin_kegiatan = IzinKegiatan.objects.filter(user__profile__role = 'MAHASISWA')
        izin_kegiatan_serialized = IzinKegiatanMahasiswaSerializer(list_izin_kegiatan, many=True)
        return JsonResponse(izin_kegiatan_serialized.data, safe=False)
    
    #case for else
    data = {
        'message' : 'invalid API call'
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])  
def detail_izin_kegiatan(request,pk):
    try:
        izin_kegiatan = IzinKegiatan.objects.get(pk=pk)
    except IzinKegiatan.DoesNotExist:
        return JsonResponse({'message': 'Izin kegiatan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        izin_kegiatan_serialized = IzinKegiatanMahasiswaSerializer(izin_kegiatan)
        return JsonResponse(izin_kegiatan_serialized.data, safe=False)
    data = {
            'message' : 'invalid API call'
        }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])
def get_list_perizinan_PKM(request):
    if request.method == 'GET':
        list_izin_kegiatan = IzinKegiatan.objects.filter(status_perizinan_kegiatan=1)
        list_izin_kegiatan_serialized = IzinKegiatanMahasiswaSerializer(list_izin_kegiatan, many=True)
        return JsonResponse(list_izin_kegiatan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET',])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])
def get_list_perizinan_PKM_Verified(request):
    if request.method == 'GET':
        list_izin_kegiatan = IzinKegiatan.objects.filter(status_perizinan_kegiatan=2)
        list_izin_kegiatan_serialized = IzinKegiatanMahasiswaSerializer(list_izin_kegiatan, many=True)
        return JsonResponse(list_izin_kegiatan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET',])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])
def get_list_perizinan_PKM_Verified_Simplified(request):
    if request.method == 'GET':
        list_izin_kegiatan = IzinKegiatan.objects.filter(status_perizinan_kegiatan=2)
        list_izin_kegiatan_serialized = IzinKegiatanSimpliest(list_izin_kegiatan, many=True)
        return JsonResponse(list_izin_kegiatan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET',])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])
def get_list_perizinan_PKM_Denied_Simplified(request):
    if request.method == 'GET':
        list_izin_kegiatan = IzinKegiatan.objects.filter(status_perizinan_kegiatan=3)
        list_izin_kegiatan_serialized = IzinKegiatanSimpliest(list_izin_kegiatan, many=True)
        return JsonResponse(list_izin_kegiatan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET',])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])
def get_list_perizinan_PKM_Waiting_Simplified(request):
    if request.method == 'GET':
        list_izin_kegiatan = IzinKegiatan.objects.filter(status_perizinan_kegiatan=1)
        list_izin_kegiatan_serialized = IzinKegiatanSimpliest(list_izin_kegiatan, many=True)
        return JsonResponse(list_izin_kegiatan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET',])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])
def get_list_perizinan_Humas_Waiting_Simplified(request):
    if request.method == 'GET':
        list_perizinan_publikasi= JenisIzinPublikasi.objects.filter(status_perizinan_publikasi=1)
        list_permintaan_souvenir = PermintaanSouvenir.objects.filter(status_permintaan_souvenir=1)
        list_permintaan_protokoler = PermintaanProtokoler.objects.filter(status_permintaan_protokoler=1)
        panjang = len(list_perizinan_publikasi) + len(list_permintaan_souvenir) + len(list_permintaan_protokoler)
        return JsonResponse({'length': panjang}, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET',])
@permission_classes([AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM])
def get_list_souvenir_simple(request):
    if request.method == 'GET':
        list_souvenir = Souvenir.objects.all()
        list_souvenir_serialized = SouvenirSerializerSimpliest(list_souvenir, many=True)

        return JsonResponse(list_souvenir_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

