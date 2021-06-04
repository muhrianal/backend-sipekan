from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser, MultiPartParser 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from ..permissions import AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM
from ..models.profile import Profile
from ..models.peminjaman_ruangan import PeminjamanRuangan, Perulangan
from ..models.peminjaman_ruangan import Ruangan
from ..models.izin_kegiatan import IzinKegiatan
from ..serializers.peminjaman_ruangan_serializer import PeminjamanRuanganUnitKerjaSerializer, IzinKegiatanUnitKerjaSerializer
from django.http.response import JsonResponse
from ..serializers.peminjaman_ruangan_serializer import PeminjamanRuanganSerializer, PerulanganSerializer
from ..serializers.kalender_serializer import KalenderSerializer
from ..serializers.peminjaman_ruangan_serializer import PeminjamanRuanganSerializer, RuanganSerializer
from ..serializers.peminjaman_ruangan_serializer import PeminjamanRuanganMahasiswaSerializer
from ..serializers.peminjaman_ruangan_serializer import PeminjamanRuanganSerializer, RuanganSerializer, IzinKegiatanFasturSerializer
import datetime
from .utils_peminjaman_ruangan import is_available

@api_view(['PUT',])
@permission_classes([permissions.AllowAny,]) #nanti diganti jadi admin fastur dan peminjam
def update_peminjaman_ruangan_by_id_peminjaman_ruangan(request, id_peminjaman):
    try:
        peminjaman_ruangan = PeminjamanRuangan.objects.get(pk=id_peminjaman)
    except:
        return JsonResponse({'message': 'Peminjaman ruangan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        
        peminjaman_data = JSONParser().parse(request) 
        # print(peminjaman_data['alasan_penolakan'])

        try:
            peminjaman_ruangan.status_peminjaman_ruangan = peminjaman_data['status_peminjaman_ruangan']
            if peminjaman_data['alasan_penolakan'] is not None:
                peminjaman_ruangan.alasan_penolakan = peminjaman_data['alasan_penolakan']
            peminjaman_ruangan.save()
            return JsonResponse(PeminjamanRuanganUnitKerjaSerializer(peminjaman_ruangan).data, safe=False)
        except:
            return JsonResponse({'message': 'Terjadi kesalahan'}, status=status.HTTP_400_BAD_REQUEST)

            

        return JsonResponse({'message': 'Terjadi kesalahan'}, status=status.HTTP_400_BAD_REQUEST) 
    
    #case for else
    data = {
        'message' : 'invalid API method'
    }
    return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([permissions.AllowAny,])
def list_jadwal(request):

    if request.method == 'GET':
        list_jadwal = PeminjamanRuangan.objects.all()
        list_jadwal_serialized = KalenderSerializer(list_jadwal, many=True)
        return JsonResponse(list_jadwal_serialized.data, safe=False)
    
    #case for else
    data = {
        'message' : 'invalid API call'
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny,])
def list_peminjaman_ruangan(request):

    if request.method == 'GET':
        list_peminjaman_ruangan = PeminjamanRuangan.objects.all()
        peminjaman_ruangan_serialized = PeminjamanRuanganSerializer(list_peminjaman_ruangan, many=True)
        return JsonResponse(peminjaman_ruangan_serialized.data, safe=False)

    #case for else
    data = {
        'message' : 'invalid API call'
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny,])
def list_ruangan(request):
    if request.method == 'GET':
        daftar_ruangan = Ruangan.objects.all()
        ruangans_serialized = RuanganSerializer(daftar_ruangan, many= True)
        return JsonResponse(ruangans_serialized.data, safe=False)
#     data = {
#             'message' : 'invalid API call'
#         }
#     return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        ruang_data = JSONParser().parse(request)
        ruang_serializer = RuanganSerializer(data=ruang_data)
        if ruang_serializer.is_valid():
            ruang_serializer.save()
            return JsonResponse(ruang_serializer.data, status=status.HTTP_201_CREATED)
        data = {
                    'message' : 'invalid API call'
                }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
@permission_classes([permissions.AllowAny,])
def detail_ruangan(request,pk):
    try:
        ruangan = Ruangan.objects.get(pk=pk)
    except Ruangan.DoesNotExist:
        return JsonResponse({'message': 'Ruangan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ruangan_serialized = RuanganSerializer(ruangan)
        return JsonResponse(ruangan_serialized.data, safe=False)
#     data = {
#             'message' : 'invalid API call'
#         }
#     return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
            ruangan_data = JSONParser().parse(request)
            ruangan_serializer = RuanganSerializer(ruangan, data=ruangan_data)
            if ruangan_serializer.is_valid():
                ruangan_serializer.save()
                return JsonResponse(ruangan_serializer.data)
            return JsonResponse(ruangan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        ruangan.delete()
        return JsonResponse({'messagee': 'Ruangan berhasil dihapus'}, status=status.HTTP_204_NO_CONTENT)
#         #do something untuk request DELETE, misal hapus izin kegiatan yang sudah ada
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 
 
@api_view(['POST',])
@permission_classes([permissions.AllowAny,]) #nanti diganti jadi unit kerja
def post_peminjaman_ruangan_unit_kerja(request):
    if request.method == 'POST':
        peminjaman_data = JSONParser().parse(request)
        
        peminjaman_data_serialized = IzinKegiatanUnitKerjaSerializer(data=peminjaman_data)
        if peminjaman_data_serialized.is_valid():
            if not is_available(peminjaman_data):
                return JsonResponse({'message' : 'Ruangan tidak tersedia'}, status=status.HTTP_409_CONFLICT)


            print('masuk sini')
            peminjaman_data_serialized.save()
            return JsonResponse(peminjaman_data_serialized.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(peminjaman_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET',])
@permission_classes([permissions.AllowAny,])
def get_list_perizinan_fastur(request):
    if request.method == 'GET':
        list_izin_kegiatan = IzinKegiatan.objects.filter(status_perizinan_kegiatan=2)
        list_izin_kegiatan_serialized = IzinKegiatanFasturSerializer(list_izin_kegiatan, many=True)
        return JsonResponse(list_izin_kegiatan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny,]) #nanti diganti jadi mahasiswa
def post_peminjaman_ruangan_mahasiswa(request,id_izin_kegiatan):
    try: 
        izin_kegiatan = IzinKegiatan.objects.get(pk=id_izin_kegiatan)
    except:
        return JsonResponse({'message': 'Izin kegiatan tidak ada'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        peminjaman_data = JSONParser().parse(request)
        peminjaman_ruangan_serialized =PeminjamanRuanganMahasiswaSerializer(izin_kegiatan,data=peminjaman_data)
        if peminjaman_ruangan_serialized.is_valid():
            peminjaman_ruangan_serialized.save()
            return JsonResponse(peminjaman_ruangan_serialized.data)
        return JsonResponse(peminjaman_ruangan_serialized.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET',])
@permission_classes([permissions.AllowAny,])
def get_peminjaman_ruangan_by_id_izin_kegiatan(request, id_izin_kegiatan):
    if request.method == 'GET':
        list_peminjaman_ruangan = PeminjamanRuangan.objects.filter(izin_kegiatan_id = id_izin_kegiatan)
        list_peminjaman_ruangan_serialized = PeminjamanRuanganUnitKerjaSerializer(list_peminjaman_ruangan, many=True)
        return JsonResponse(list_peminjaman_ruangan_serialized.data, safe=False)
    
    #case for else
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET','PUT'])
@permission_classes([permissions.AllowAny,])
def detail_peminjaman_ruangan(request,pk):
    try:
        peminjaman_ruangan = PeminjamanRuangan.objects.get(pk=pk)
    except PeminjamanRuangan.DoesNotExist:
        return JsonResponse({'message': 'Peminjaman Ruangan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        peminjaman_ruangan_serialized = PeminjamanRuanganSerializer(peminjaman_ruangan)
        return JsonResponse(peminjaman_ruangan_serialized.data, safe=False)
    elif request.method == 'PUT':
        peminjaman_ruangan_data = JSONParser().parse(request)
        peminjaman_ruangan_serializer = PeminjamanRuanganSerializer(peminjaman_ruangan, data=peminjaman_ruangan_data)
        if peminjaman_ruangan_serializer.is_valid():
            peminjaman_ruangan_serializer.save()
            return JsonResponse(peminjaman_ruangan_serializer.data)
        return JsonResponse(peminjaman_ruangan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','PUT'])
@permission_classes([permissions.AllowAny,])
def perulangan(request,pk):
    try:
        perulangan = Perulangan.objects.get(pk=pk)
    except Perulangan.DoesNotExist:
        return JsonResponse({'message': 'Perulangan tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        perulangan_serialized = PerulanganSerializer(perulangan)
        return JsonResponse(perulangan_serialized.data, safe=False)
    elif request.method == 'PUT':
        perulangan_data = JSONParser().parse(request)
        perulangan_serializer = PerulanganSerializer(perulangan, data=perulangan_data)
        if perulangan_serializer.is_valid():
            perulangan_serializer.save()
            return JsonResponse(perulangan_serializer.data)
        return JsonResponse(perulangan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message' : 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
