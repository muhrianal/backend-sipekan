
from rest_framework import serializers 

from django.contrib.auth.models import User
from ..models.izin_kegiatan import IzinKegiatan
from django.contrib.auth.models import User
from rest_framework import serializers
from ..models.peminjaman_ruangan import Ruangan


from ..models.profile import Profile
from ..models.izin_kegiatan import IzinKegiatan
from ..models.izin_kegiatan import DetailKegiatan
from ..models.peminjaman_ruangan import PeminjamanRuangan, Perulangan
from ..models.humas import PermintaanProtokoler, PerizinanPublikasi, PermintaanSouvenir, JenisPublikasi, JenisIzinPublikasi

#Nama kelas dibawah ini di rename, yang terkati dengan kelas ini harus diperbarui
class RuanganSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ruangan
        fields = ['id', 'nama']
class IzinKegiatanSerializerSimplified(serializers.ModelSerializer):

    class Meta:
        model = IzinKegiatan
        fields = '__all__'

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

    perulangan = PerulanganSerializer()
    class Meta:
        model = PeminjamanRuangan
        fields = ('id', 'judul_peminjaman', 'jumlah_peserta','status_peminjaman_ruangan',
        'alasan_penolakan', 'waktu_mulai','waktu_akhir','catatan','ruangan','terbuka_untuk_umum','perulangan')


class PermintaanProtokolerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermintaanProtokoler
        fields = '__all__'

class JenisPublikasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisPublikasi
        fields = '__all__'

class JenisIzinPublikasiHumasSerializer(serializers.ModelSerializer): # untuk verifikasi perizinan publikasi oleh admin humas
    jenis_publikasi = JenisPublikasiSerializer(read_only=True)
    class Meta:
        model = JenisIzinPublikasi
        fields = '__all__'  

class JenisIzinPublikasiSerializer(serializers.ModelSerializer): # untuk post perizinan publikasi oleh mahasiswa
    class Meta:
        model = JenisIzinPublikasi
        fields = ('jenis_publikasi','status_perizinan_publikasi','alasan_penolakan')
    
    def update(self, perizinan_publikasi, validated_data):
        JenisIzinPublikasi.objects.create(perizinan_publikasi=perizinan_publikasi, **validated_data)
        return perizinan_publikasi
 
class PerizinanPublikasiHumasSerializer(serializers.ModelSerializer): # untuk verifikasi perizinan publikasi oleh admin humas
    jenis_izin_publikasi = JenisIzinPublikasiHumasSerializer(read_only=True,many=True)
    class Meta:
        model = PerizinanPublikasi
        fields = '__all__'

class PerizinanPublikasiSerializer(serializers.ModelSerializer): # untuk post perizinan publikasi oleh mahasiswa
    class Meta:
        model = PerizinanPublikasi
        fields = ('id','tanggal_mulai', 'tanggal_akhir','keterangan', 'file_materi_kegiatan', 'file_flyer_pengumuman','izin_kegiatan')
  

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

    detail_kegiatan = DetailKegiatanSerializer(read_only=True)
    peminjaman_ruangan = PeminjamanRuanganSerializer(many=True, read_only=True)
    permintaan_protokoler = PermintaanProtokolerSerializer(read_only=True)
    perizinan_publikasi = PerizinanPublikasiHumasSerializer(read_only=True)
    permintaan_souvenir = PermintaanSouvenirSerializer(many=True, read_only=True)

    class Meta:
        model = IzinKegiatan
        fields = ('id','nama_kegiatan', 'organisasi', 'user', 'status_perizinan_kegiatan','detail_kegiatan','peminjaman_ruangan','permintaan_protokoler','perizinan_publikasi','permintaan_souvenir')

class DetailKegiatanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DetailKegiatan
        fields = '__all__'

class DetailIzinKegiatanSerializer(serializers.ModelSerializer):

    # detail_kegiatan = DetailKegiatanSerializer(read_only=True)

    class Meta:
        model = IzinKegiatan
        fields = ('id','nama_kegiatan', 'organisasi', 'user', 'status_perizinan_kegiatan','detail_kegiatan')
    
    def update(self,instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.nama_kegiatan = validated_data.get('nama_keegiatan', instance.nama_kegiatan)
        instance.organisasi = validated_data.get('organisasi', instance.organisasi)
        instance.user = validated_data.get('user', instance.user)
        instance.status_perizinan_kegiatan = validated_data.get('status_perizinan_kegiatan', instance.status_perizinan_kegiatan)
        instance.save()

        detail = validated_data.get('detail_kegiatan')

        detail_id = detail.get('id', None)
        if detail_id:
            detail_izin = DetailKegiatan.objects.get(id=detail_id, izin_kegiatan = instance)
            detail_izin.waktu_tanggal_mulai = detail.get('waktu_tanggal_mulai', instance.waktu_tanggal_mulai)
            detail_izin.waktu_tanggal_akhir = detail.get('waktu_tanggal_akhir', instance.waktu_tanggal_akhir)
            detail_izin.email_pic = detail.get('email_pic', instance.email_pic)
            detail_izin.nama_pic = detail.get('nama_pic', instance.nama_pic)
            detail_izin.hp_pic = detail.get('hp_pic', instance.hp_pic)
            detail_izin.npm_pic = detail.get('npm_pic', instance.npm_pic)
            detail_izin.npm_ketua_organisasi = detail.get('npm_ketua_organisasi', instance.npm_ketua_organisasi)
            detail_izin.nama_ketua_organisasi = detail.get('nama_ketua_organisasi', instance.nama_ketua_organisasi)
            detail_izin.tempat_pelaksanaan = detail.get('tempat_pelaksanaan', instance.tempat_pelaksanaan)
            detail_izin.sumber_pendanaan = detail.get('sumber_pendanaan', instance.sumber_pendanaan)
            detail_izin.alasan_penolakan = detail.get('alasan_penolakan', instance.alasan_penolakan)
            detail_izin.file_info_kegiatan = detail.get('file_info_kegiatan', detainstanceil_izin.file_info_kegiatan)
            detail_izin.created_at = detail.get('created_at' ,instance.created_at)
            detail_izin.updated_at = detail.get('updated_at', instance.updated_at)
            detai_izin.save()

        return instance

        # if 'detail_kegiatan' in validated_data:
        #     nested_serializer = self.fields['detail_kegiatan']
        #     nested_instance = instance.detail_kegiatan
        #     nested_data = validated_data.pop('detail_kegiatan')

        #     nested_serializer.update(nested_instance, nested_data)

        # return super(DetailIzinKegiatanSerializer, self).update(instance, validated_data)

        # detail_kegiatan_data = validated_data.pop('detail_kegiatan')
        # detail_kegiatan = izin_kegiatan.detail_kegiatan
        # izin_kegiatan.save()
        # detail_kegiatan.save()
        # return izin_kegiatan
        # izin_kegiatan = IzinKegiatan.objects.update(**validated_data)
        # DetailKegiatan.objects.update(izin_kegiatan = izin_kegiatan, **detail_kegiatan_data)
        # return izin_kegiatan


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
        fields = ['id', 'username', 'profile']

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

class PeminjamanRuanganSerializerDetailed(serializers.ModelSerializer):
    ruangan = RuanganSerializer()

    class Meta:
        model = PeminjamanRuangan
        fields = (
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
        )

class IzinKegiatanSerializerDetailed(serializers.ModelSerializer):

    peminjaman_ruangan = PeminjamanRuanganSerializerDetailed(many=True, read_only=True)
    permintaan_protokoler = PermintaanProtokolerSerializer(read_only=True)
    perizinan_publikasi = PerizinanPublikasiSerializer(read_only=True)
    permintaan_souvenir = PermintaanSouvenirSerializer(many=True, read_only=True)

    class Meta:
        model = IzinKegiatan
        fields = ('id','nama_kegiatan', 'organisasi', 'user', 'status_perizinan_kegiatan','detail_kegiatan','peminjaman_ruangan','permintaan_protokoler','perizinan_publikasi','permintaan_souvenir')

class DetailKegiatanSimpliest(serializers.ModelSerializer):
    
    class Meta:    
        model = DetailKegiatan
        fields =( 
            'waktu_tanggal_mulai', 
        )

class IzinKegiatanSimpliest(serializers.ModelSerializer):
    detail_kegiatan = DetailKegiatanSimpliest()
    class Meta:
        model = IzinKegiatan
        fields = ('nama_kegiatan', 'status_perizinan_kegiatan', 'detail_kegiatan')

class IzinKegiatanMahasiswaSerializer1(serializers.ModelSerializer):
    detail_kegiatan = DetailKegiatanMahasiswaSerializer()
    user = UserSerializer()
    
    class Meta:
        model = IzinKegiatan
        fields = ('id','nama_kegiatan', 'organisasi', 'user', 'status_perizinan_kegiatan','detail_kegiatan')