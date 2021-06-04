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

from ..permissions import AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM, AllowOnlyMahasiswa

from ..models.humas import PerizinanPublikasi, PermintaanProtokoler, PermintaanSouvenir, JenisPublikasi, Souvenir, JenisIzinPublikasi
from ..models.izin_kegiatan import IzinKegiatan

from ..serializers.humas_serializer import PermintaanSouvenirHumasSerializer,PerizinanPublikasiSerializer,PermintaanProtokolerSerializer, PerizinanKegiatanSerializer, JenisPublikasiSerializer,SouvenirSerializer,PerizinanPublikasiSerializer,  PerizinKegiatanHumasSerializer,  JenisIzinPublikasiSerializer,JenisIzinPublikasiHumasSerializer, PermintaanSouvenirSerializer

from django.utils import timezone
from django.http.response import JsonResponse
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET'])
@permission_classes([permissions.AllowAny,]) #admin humas
def get_list_perizinan_humas(request): 
    if request.method == 'GET': # get list seluruh izin kegiatan (humas)
        list_izin_kegiatan = IzinKegiatan.objects.filter(status_perizinan_kegiatan=2)
        list_izin_kegiatan_serialized = PerizinKegiatanHumasSerializer(list_izin_kegiatan, many=True)
        return JsonResponse(list_izin_kegiatan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny,]) #mahasiswa dan admin humas
def get_post_perizinan_humas_by_id_izin_kegiatan(request,id_izin_kegiatan):
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

    if request.method == 'GET':  # get izin kegiatan (humas)
        detail_perizinan_humas_kegiatan_serialized =  PerizinKegiatanHumasSerializer(izin_kegiatan)
        return JsonResponse(detail_perizinan_humas_kegiatan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT',])
@permission_classes([permissions.AllowAny,]) #admin humas 
def update_permintaan_souvenir_by_id_permintaan_souvenir(request, id_permintaan):
    try:
        permintaan_souvenir =PermintaanSouvenir.objects.get(pk=id_permintaan)
    except:
        return JsonResponse({'message': 'Permintaan souvenir tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        peminjaman_data = JSONParser().parse(request) 
        try:
            permintaan_souvenir.status_permintaan_souvenir = peminjaman_data['status_permintaan_souvenir']
            permintaan_souvenir.updated_at = timezone.now()
            if peminjaman_data['alasan_penolakan'] is not None:
               permintaan_souvenir.alasan_penolakan = peminjaman_data['alasan_penolakan']
            permintaan_souvenir.save()
            return JsonResponse(PermintaanSouvenirHumasSerializer(permintaan_souvenir).data, safe=False)
        except:
            return JsonResponse({'message': 'Terjadi kesalahan'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': 'Terjadi kesalahan'}, status=status.HTTP_400_BAD_REQUEST) 
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT',])
@permission_classes([permissions.AllowAny,]) #admin humas
def update_permintaan_protokoler_by_id_permintaan_protokoler(request, id_permintaan):
    try:
        permintaan_protokoler = PermintaanProtokoler.objects.get(pk=id_permintaan)
    except:
        return JsonResponse({'message': 'Permintaan protokoler tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        peminjaman_data = JSONParser().parse(request) 
        try:
            permintaan_protokoler.status_permintaan_protokoler = peminjaman_data['status_permintaan_protokoler']
            permintaan_protokoler.updated_at = timezone.now()
            if peminjaman_data['alasan_penolakan'] is not None:
               permintaan_protokoler.alasan_penolakan = peminjaman_data['alasan_penolakan']
            permintaan_protokoler.save()
            return JsonResponse(PermintaanProtokolerSerializer(permintaan_protokoler).data, safe=False)
        except:
            return JsonResponse({'message': 'Terjadi kesalahan'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': 'Terjadi kesalahan'}, status=status.HTTP_400_BAD_REQUEST) 
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT',])
@permission_classes([permissions.AllowAny,]) #nanti diganti jadi admin humas
def update_jenis_izin_publikasi_by_id_jenis_izin_publikasi(request, id_jenis_izin_publikasi):
    try:
        jenis_izin_publikasi = JenisIzinPublikasi.objects.get(pk=id_jenis_izin_publikasi)
    except:
        return JsonResponse({'message': 'Jenis izin publikasi tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        perizinan_data = JSONParser().parse(request) 
        try:
            jenis_izin_publikasi.status_perizinan_publikasi = perizinan_data['status_perizinan_publikasi']
            if perizinan_data['alasan_penolakan'] is not None:
                jenis_izin_publikasi.alasan_penolakan = perizinan_data['alasan_penolakan']
            jenis_izin_publikasi.save()
            jenis_izin_publikasi_serialized = JenisIzinPublikasiHumasSerializer(jenis_izin_publikasi)
            try:
                perizinan_publikasi = PerizinanPublikasi.objects.get(pk=perizinan_data['id_perizinan_publikasi'])
                perizinan_publikasi.updated_at= timezone.now()
                perizinan_publikasi.save()
            except:
                pass
            return JsonResponse(JenisIzinPublikasiHumasSerializer(jenis_izin_publikasi).data, safe=False)
        except:
            return JsonResponse({'message': 'Terjadi kesalahan'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': 'Terjadi kesalahan'}, status=status.HTTP_400_BAD_REQUEST) 
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny,]) #mahasiswa
@parser_classes([MultiPartParser, FormParser])
def post_perizinan_publikasi(request):
    if request.method == 'POST': # post perizinan_publikasi
        perizinan_data_serialized = PerizinanPublikasiSerializer(data=request.data)
        if perizinan_data_serialized.is_valid():
            perizinan_data_serialized.save()
            
            # menyimpan jenis_izin_publikasi dari list jenis_publikasi
            jenis_publikasi_string = request.data['jenis_publikasi']
            print(request.data['jenis_publikasi'])
            print(jenis_publikasi_string)
            if jenis_publikasi_string != '':
                jenis_publikasi_list = [data.strip() for data in jenis_publikasi_string.split(',')]
                for jenis_publikasi in jenis_publikasi_list: # menyimpan setiap jenis_izin_publikasi
                    jenis_izin_publikasi_data = {
                        "jenis_publikasi" : jenis_publikasi,
                        "status_perizinan_publikasi": "1",
                        "alasan_penolakan": ''
                    }
                    jenis_izin_publikasi_serialized = JenisIzinPublikasiSerializer(PerizinanPublikasi.objects.last(),data=jenis_izin_publikasi_data)
                    if jenis_izin_publikasi_serialized.is_valid():
                        jenis_izin_publikasi_serialized.save()
            
            return JsonResponse(perizinan_data_serialized.data,status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(perizinan_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([permissions.AllowAny,]) #mahasiswa dan admin humas
def get_jenis_publikasi(request):
    if request.method == 'GET':
        list_jenis_publikasi = JenisPublikasi.objects.all()
        list_jenis_publikasi_serialized = JenisPublikasiSerializer(list_jenis_publikasi, many=True)
        return JsonResponse(list_jenis_publikasi_serialized.data,safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([permissions.AllowAny,]) # mahasiswa dan admin humas
def get_list_souvenir(request):
    if request.method == 'GET':
        list_souvenir = Souvenir.objects.all()
        list_souvenir_serialized = SouvenirSerializer(list_souvenir, many=True)
        return JsonResponse(list_souvenir_serialized.data,safe=False)

    
    #case for else

    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowOnlyAdminHUMAS])
def post_souvenir(request):
    if request.method == 'POST':
        souvenir_data = JSONParser().parse(request)
        souvenir_serializer = SouvenirSerializer(data=souvenir_data)
        if souvenir_serializer.is_valid():
            souvenir_serializer.save()
            return JsonResponse(souvenir_serializer.data, status=status.HTTP_201_CREATED)
        data = {
                    'message' : 'invalid API call'
                }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
@permission_classes([AllowOnlyAdminHUMAS])
def detail_souvenir(request,pk):
    try:
        souvenir = Souvenir.objects.get(pk=pk)
    except Souvenir.DoesNotExist:
        return JsonResponse({'message': 'Souvenir tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        souvenir_serialized = SouvenirSerializer(souvenir)
        return JsonResponse(souvenir_serialized.data, safe=False)
#     data = {
#             'message' : 'invalid API call'
#         }
#     return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
            souvenir_data = JSONParser().parse(request)
            souvenir_serializer = SouvenirSerializer(souvenir, data=souvenir_data)
            if souvenir_serializer.is_valid():
                souvenir_serializer.save()
                return JsonResponse(souvenir_serializer.data)
            return JsonResponse(souvenir_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        souvenir.delete()
        return JsonResponse({'message': 'Souvenir berhasil dihapus'}, status=status.HTTP_204_NO_CONTENT)
#         #do something untuk request DELETE, misal hapus izin kegiatan yang sudah ada
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 

@api_view(['GET','PUT'])
@permission_classes([permissions.AllowAny,])
def detail_permintaan_protokoler(request,pk):
    try:
        permintaan_protokoler = PermintaanProtokoler.objects.get(pk=pk)
    except PermintaanProtokoler.DoesNotExist:
        return JsonResponse({'message': 'Permintaan protokoler tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        permintaan_protokoler_serialized = PermintaanProtokolerSerializer(permintaan_protokoler)
        return JsonResponse(permintaan_protokoler_serialized.data, safe=False)
    # data = {
    #         'message' : 'invalid API call'
    #     }
    elif request.method == 'PUT':
            permintaan_protokoler_data = JSONParser().parse(request)
            permintaan_protokoler_serializer = PermintaanProtokolerSerializer(permintaan_protokoler, data=permintaan_protokoler_data)
            if permintaan_protokoler_serializer.is_valid():
                permintaan_protokoler_serializer.save()
                return JsonResponse(permintaan_protokoler_serializer.data)
            return JsonResponse(permintaan_protokoler_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         #do something untuk request DELETE, misal hapus izin kegiatan yang sudah ada
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 

@api_view(['GET','PUT'])
@permission_classes([permissions.AllowAny,])
def detail_permintaan_souvenir(request,pk):
    try:
        permintaan_souvenir = PermintaanSouvenir.objects.get(pk=pk)
    except PermintaanSouvenir.DoesNotExist:
        return JsonResponse({'message': 'Ruangan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        permintaan_souvenir_serialized = PermintaanSouvenirSerializer(permintaan_souvenir)
        return JsonResponse(permintaan_souvenir_serialized.data, safe=False)
    elif request.method == 'PUT':
        permintaan_souvenir_data = JSONParser().parse(request)
        permintaan_souvenir_serializer = PermintaanSouvenirSerializer(permintaan_souvenir, data=permintaan_souvenir_data)
        if permintaan_souvenir_serializer.is_valid():
            permintaan_souvenir_serializer.save()
            return JsonResponse(permintaan_souvenir_serializer.data)
        return JsonResponse(permintaan_souvenir_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 

@api_view(['PUT'])
@permission_classes([AllowOnlyMahasiswa]) 
@parser_classes([MultiPartParser, FormParser])
def put_perizinan_publikasi(request, pk):
    try:
        perizinan_publikasi = PerizinanPublikasi.objects.get(pk=pk)
    except PermintaanSouvenir.DoesNotExist:
        return JsonResponse({'message': 'perizinan publikasi tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT': # post perizinan_publikasi
        perizinan_data_serialized = PerizinanPublikasiSerializer(perizinan_publikasi, data=request.data)
        if perizinan_data_serialized.is_valid():
            perizinan_data_serialized.save()
            
            # menyimpan jenis_izin_publikasi dari list jenis_publikasi
            jenis_publikasi_string = request.data['jenis_publikasi']
            print(request.data['jenis_publikasi'])
            print(jenis_publikasi_string)
            if jenis_publikasi_string != '':
                jenis_publikasi_list = [data.strip() for data in jenis_publikasi_string.split(',')]
                for jenis_publikasi in jenis_publikasi_list: # menyimpan setiap jenis_izin_publikasi
                    jenis_izin_publikasi_data = {
                        "jenis_publikasi" : jenis_publikasi,
                        "status_perizinan_publikasi": "1",
                        "alasan_penolakan": ''
                    }
                    jenis_izin_publikasi_serialized = JenisIzinPublikasiSerializer(PerizinanPublikasi.objects.last(),data=jenis_izin_publikasi_data)
                    if jenis_izin_publikasi_serialized.is_valid():
                        jenis_izin_publikasi_serialized.save()
            
            return JsonResponse(perizinan_data_serialized.data,status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(perizinan_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

