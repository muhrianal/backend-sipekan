from rest_framework import serializers 
from ..models.peminjaman_ruangan import PeminjamanRuangan, Perulangan
from ..models.peminjaman_ruangan import Ruangan
from ..models.izin_kegiatan import IzinKegiatan
from ..models.profile import Profile
from django.contrib.auth.models import User


class PerulanganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perulangan
        fields = [
            'id',
            'jenjang',
            'tanggal_mulai',
            'tanggal_akhir',
        ]



class PeminjamanRuanganSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PeminjamanRuangan

        fields = '__all__'


class PeminjamanRuanganUnitKerjaSerializer(serializers.ModelSerializer):
    perulangan = PerulanganSerializer()
    
    class Meta:
        model = PeminjamanRuangan

        fields = [
            "id",
            "judul_peminjaman",
            "jumlah_peserta",
            "status_peminjaman_ruangan",
            "alasan_penolakan",
            "waktu_mulai",
            "waktu_akhir",
            "catatan",
            "created_at",
            "updated_at",
            "ruangan",
            "terbuka_untuk_umum",
            "perulangan",

        ]

class PeminjamanRuanganSerializer(serializers.ModelSerializer):

    class Meta:
        model = PeminjamanRuangan
        fields = '__all__'

class RuanganSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ruangan
        fields = '__all__'



class IzinKegiatanUnitKerjaSerializer(serializers.ModelSerializer):
    peminjaman_ruangan = PeminjamanRuanganUnitKerjaSerializer(many=True)
    
    class Meta:
        model = IzinKegiatan
        fields = ('id', 'nama_kegiatan', 'organisasi', 'user', 'status_perizinan_kegiatan', 'peminjaman_ruangan')

    def create(self, validated_data):
        peminjaman_ruangan_data = validated_data.pop('peminjaman_ruangan')
        
        izin_kegiatan = IzinKegiatan.objects.create(**validated_data)
        for peminjaman_ruangan in peminjaman_ruangan_data:
            perulangan_data = peminjaman_ruangan.pop('perulangan')
            peminjaman_ruangan_created = PeminjamanRuangan.objects.create(izin_kegiatan=izin_kegiatan, **peminjaman_ruangan)
            Perulangan.objects.create(peminjaman_ruangan=peminjaman_ruangan_created, **perulangan_data)
        return izin_kegiatan

class PeminjamanRuanganMahasiswa(serializers.ModelSerializer):
    perulangan = PerulanganSerializer()
    class Meta:
        model = PeminjamanRuangan
        fields = ('id', 'judul_peminjaman', 'status_peminjaman_ruangan',
        'alasan_penolakan', 'waktu_mulai','waktu_akhir','catatan','ruangan','perulangan')


class PeminjamanRuanganMahasiswaSerializer(serializers.ModelSerializer):
    peminjaman_ruangan = PeminjamanRuanganUnitKerjaSerializer(many=True)

    class Meta: 
        model = IzinKegiatan
        fields = ('id','peminjaman_ruangan')

    def update(self,izin_kegiatan,validated_data):
        peminjaman_ruangan_data = validated_data.pop('peminjaman_ruangan')
        for peminjaman_ruangan in peminjaman_ruangan_data:
            # print("peminjaman data " + peminjaman_ruangan_data)
            # print("peminjaman " + peminjaman_ruangan)
            perulangan = peminjaman_ruangan.pop('perulangan')
            peminjaman_ruangan_created = PeminjamanRuangan.objects.create(izin_kegiatan=izin_kegiatan, **peminjaman_ruangan)
            Perulangan.objects.create(peminjaman_ruangan=peminjaman_ruangan_created, **perulangan)
        return izin_kegiatan
    


# class ProfileSefri
class PeminjamanRuanganFasturSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeminjamanRuangan
        fields = ['id', 'status_peminjaman_ruangan']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']

class IzinKegiatanFasturSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    peminjaman_ruangan = PeminjamanRuanganFasturSerializer(many=True)
    
    class Meta:
        model = IzinKegiatan
        fields = ('id', 'nama_kegiatan', 'organisasi', 'status_perizinan_kegiatan', 'user', 'peminjaman_ruangan')
