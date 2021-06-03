
from rest_framework import serializers 

from django.contrib.auth.models import User
from ..models.izin_kegiatan import IzinKegiatan
from django.contrib.auth.models import User
from rest_framework import serializers

from ..models.profile import Profile
from ..models.izin_kegiatan import IzinKegiatan
from ..models.izin_kegiatan import DetailKegiatan
from ..models.peminjaman_ruangan import PeminjamanRuangan
from ..models.humas import PermintaanProtokoler, PerizinanPublikasi, PermintaanSouvenir

#Nama kelas dibawah ini di rename, yang terkati dengan kelas ini harus diperbarui
class IzinKegiatanSerializerSimplified(serializers.ModelSerializer):

    class Meta:
        model = IzinKegiatan
        fields = '__all__'

class PeminjamanRuanganSerializer(serializers.ModelSerializer):


    class Meta:
        model = PeminjamanRuangan
        fields = '__all__'

class PermintaanProtokolerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermintaanProtokoler
        fields = '__all__'

class PerizinanPublikasiSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerizinanPublikasi
        fields = '__all__'

class PermintaanSouvenirSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermintaanSouvenir
        fields = '__all__'

class DetailKegiatanSerializer(serializers.ModelSerializer):

    class Meta:
            model = DetailKegiatan
            fields =(
                'id',
                'waktu_tanggal_mulai',
                'waktu_tanggal_akhir',
                'email_pic',
                'nama_pic',
                'hp_pic',
                'npm_pic',
                'npm_ketua_organisasi',
                'nama_ketua_organisasi',
                'tempat_pelaksanaan',
                'sumber_pendanaan',
                'alasan_penolakan',
                'file_info_kegiatan',
                'created_at',
                'updated_at',
                'izin_kegiatan'
            )

class IzinKegiatanSerializer(serializers.ModelSerializer):

    peminjaman_ruangan = PeminjamanRuanganSerializer(many=True, read_only=True)
    permintaan_protokoler = PermintaanProtokolerSerializer(read_only=True)
    perizinan_publikasi = PerizinanPublikasiSerializer(read_only=True)
    permintaan_souvenir = PermintaanSouvenirSerializer(many=True, read_only=True)

    class Meta:
        model = IzinKegiatan
        fields = ('id','nama_kegiatan', 'organisasi', 'user', 'status_perizinan_kegiatan','detail_kegiatan','peminjaman_ruangan','permintaan_protokoler','perizinan_publikasi','permintaan_souvenir')

class DetailKegiatanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DetailKegiatan
        fields = '__all__'

class DetailKegiatanMahasiswaSerializer(serializers.ModelSerializer):
    
    class Meta:    
        model = DetailKegiatan
        # fields = '__all__'
        fields =(
            'id',
            'waktu_tanggal_mulai',
            'waktu_tanggal_akhir',
            'email_pic',
            'nama_pic',
            'hp_pic',
            'npm_pic',
            'npm_ketua_organisasi',
            'nama_ketua_organisasi',
            'tempat_pelaksanaan',
            'sumber_pendanaan',
            'alasan_penolakan',
            'file_info_kegiatan',
            'created_at', 
            'updated_at', 
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = '__all__'

class IzinKegiatanMahasiswaSerializer(serializers.ModelSerializer):
    detail_kegiatan = DetailKegiatanMahasiswaSerializer()
    user = UserSerializer()
    
    class Meta:
        model = IzinKegiatan
        fields = ('id','nama_kegiatan', 'organisasi', 'user', 'status_perizinan_kegiatan','detail_kegiatan')

    def create(self, validated_data):
        detail_kegiatan_data = validated_data.pop('detail_kegiatan')
        izin_kegiatan = IzinKegiatan.objects.create(**validated_data)
        DetailKegiatan.objects.create(izin_kegiatan = izin_kegiatan, **detail_kegiatan_data)
        return izin_kegiatan
