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

from ..models.izin_kegiatan import DetailKegiatan, IzinKegiatan

from ..serializers.izin_kegiatan_serializer import IzinKegiatanSerializerSimplified, DetailKegiatanSerializer, IzinKegiatanMahasiswaSerializer


from django.http.response import JsonResponse


@api_view(['PUT','PATCH'])
@permission_classes([permissions.AllowAny,])
def update_izin_kegiatan_by_id_perizinan(request, id_perizinan):
    try:
        izin_kegiatan = IzinKegiatan.objects.get(pk=id_perizinan)
    except:
        return JsonResponse({'message': 'Izin kegiatan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':

        izin_data = JSONParser().parse(request) 
        izin_kegiatan_serialized = IzinKegiatanMahasiswaSerializer(izin_kegiatan, data=izin_data)
        
        if izin_kegiatan_serialized.is_valid():
            izin_kegiatan_serialized.save()
            return JsonResponse(izin_kegiatan_serialized.data)

        return JsonResponse(izin_kegiatan_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            izin_data = JSONParser().parse(request) 
            print(izin_data)
            izin_kegiatan.status_perizinan_kegiatan = izin_data["izin_kegiatan"]["status_perizinan_kegiatan"]
            if izin_data["izin_kegiatan"]["detail_kegiatan"]["alasan_penolakan"] is not None:
                izin_kegiatan.detail_kegiatan.alasan_penolakan = izin_data["izin_kegiatan"]["detail_kegiatan"]["alasan_penolakan"] 
            izin_kegiatan.save()
            izin_kegiatan_serialized = IzinKegiatanMahasiswaSerializer(izin_kegiatan)
            return JsonResponse(izin_kegiatan_serialized.data, safe=False)
        except:
           return JsonResponse(izin_kegiatan.errors, status=status.HTTP_400_BAD_REQUEST)
           
        return JsonResponse(izin_kegiatan.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        # if izin_kegiatan_serialized.is_valid():
        #     izin_kegiatan_serialized.save()
        #     return JsonResponse(izin_kegiatan_serialized.data)

        # return JsonResponse(izin_kegiatan_serialized.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 

@api_view(['POST','GET'])
@permission_classes([permissions.AllowAny,])
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