from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status, permissions
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from ..permissions import AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM, AllowOnlyMahasiswa
from ..models.profile import Profile

from django.http.response import JsonResponse
from ..models.izin_kegiatan import IzinKegiatan, DetailKegiatan
from ..serializers.izin_kegiatan_mahasiswa_serializer import IzinKegiatanMahasiswaSerializer, DetailKegiatanMahasiswaSerializer, IzinKegiatanHeaderSerialezer
from django.http.response import JsonResponse
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

#untuk izin kegiatan dengan file
@api_view(['POST'])
@permission_classes([AllowOnlyMahasiswa]) 
def post_izin_kegiatan_header(request):
    if request.method == 'POST': # post header izin kegiatan
        perizinan_data = JSONParser().parse(request)
        perizinan_data_serialized = IzinKegiatanHeaderSerialezer(data=perizinan_data)
        if perizinan_data_serialized.is_valid():
            perizinan_data_serialized.save()
            return JsonResponse(perizinan_data_serialized.data,status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(perizinan_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowOnlyMahasiswa]) 
@parser_classes([MultiPartParser, FormParser])
def post_izin_kegiatan_detail(request):
    if request.method == 'POST': # post detail izin kegiatan
        perizinan_data_serialized = DetailKegiatanMahasiswaSerializer(data=request.data)
        if perizinan_data_serialized.is_valid():
            perizinan_data_serialized.save()
            return JsonResponse(perizinan_data_serialized.data,status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(perizinan_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'GET'])
@permission_classes([permissions.AllowAny,]) #nanti diganti jadi mahasiswa
def get_put_izin_kegiatan_mahasiswa(pk,request):
    try:
        izin_kegiatan = IzinKegiatan.objects.get(pk=pk)
    except IzinKegiatan.DoesNotExist:
        return JsonResponse({'message': 'Izin Kegiatan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT': # untuk izin kegiatan tanpa file
        # perizinan_data = MultiPartParser().parse(request)
        perizinan_data = JSONParser().parse(request)
        perizinan_data_serialized = IzinSerializer(izin_kegiatan,data=perizinan_data)
        if perizinan_data_serialized.is_valid():
            perizinan_data_serialized.save()
            return JsonResponse(perizinan_data_serialized.data,status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(perizinan_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    #case for else

@api_view(['GET','PUT'])
@permission_classes([permissions.AllowAny,])
def detail_kegiatan(request,pk):
    try:
        detail_kegiatan = IzinKegiatan.objects.get(pk=pk)
    except IzinKegiatan.DoesNotExist:
        return JsonResponse({'message': 'Peminjaman Ruangan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        detail_kegiatan_serialized = DetailIzinKegiatanSerializer(detail_kegiatan)
        return JsonResponse(detail_kegiatan_serialized.data, safe=False)
    elif request.method == 'PUT':
        detail_kegiatan_data = JSONParser().parse(request)
        detail_kegiatan_serializer = DetailIzinKegiatanSerializer(detail_kegiatan, data=detail_kegiatan_data)
        if detail_kegiatan_serializer.is_valid():
            detail_kegiatan_serializer.save()
            return JsonResponse(detail_kegiatan_serializer.data)
        return JsonResponse(detail_kegiatan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

#untuk izin kegiatan dengan file
@api_view(['GET','PUT'])
@permission_classes([AllowOnlyMahasiswa]) 
def put_izin_kegiatan_header(request, pk):
    try:
        izin_kegiatan = IzinKegiatan.objects.get(pk=pk)
    except IzinKegiatan.DoesNotExist:
        return JsonResponse({'message': 'Peminjaman Ruangan tidak ada'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        izin_kegiatan_serialized = IzinKegiatanHeaderSerialezer(izin_kegiatan)
        return JsonResponse(izin_kegiatan_serialized.data, safe=False)
    elif request.method == 'PUT': # put header izin kegiatan
        perizinan_data = JSONParser().parse(request)
        perizinan_data_serialized = IzinKegiatanHeaderSerialezer(izin_kegiatan, data=perizinan_data)
        if perizinan_data_serialized.is_valid():
            perizinan_data_serialized.save()
            return JsonResponse(perizinan_data_serialized.data,status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(perizinan_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT'])
@permission_classes([AllowOnlyMahasiswa]) 
@parser_classes([MultiPartParser, FormParser])
def put_izin_kegiatan_detail(request, pk):
    try:
        detail_kegiatan = DetailKegiatan.objects.get(pk=pk)
    except DetailKegiatan.DoesNotExist:
        return JsonResponse({'message': 'Detail Kegiatan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT': 
        detail_kegiatan_serialized = DetailKegiatanMahasiswaSerializer(detail_kegiatan, data=request.data)
        
        if detail_kegiatan_serialized.is_valid():
            detail_kegiatan_serialized.save()
            return JsonResponse(detail_kegiatan_serialized.data,status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(detail_kegiatan_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
