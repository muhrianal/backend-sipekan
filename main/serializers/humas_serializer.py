from rest_framework import serializers 

from ..models.humas import PerizinanPublikasi,PermintaanSouvenir,PermintaanProtokoler, JenisPublikasi, Souvenir, JenisIzinPublikasi

from ..models.izin_kegiatan import IzinKegiatan

from .peminjaman_ruangan_serializer import UserSerializer

class SouvenirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Souvenir
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
        
class PermintaanSouvenirHumasSerializer(serializers.ModelSerializer): # untuk verifikasi permintaan souvenir oleh admin humas
    souvenir = SouvenirSerializer(read_only=True)
    class Meta:
        model = PermintaanSouvenir
        fields = '__all__'

class PermintaanSouvenirSerializer(serializers.ModelSerializer): # untuk post permintaan souvenir oleh mahasiswa
    class Meta:
        model = PermintaanSouvenir
        fields = ('id','alasan_penolakan', 'status_permintaan_souvenir', 'jumlah', 'souvenir', 
        'nama_penerima_souvenir', 'kelas_penerima_souvenir', 'region_penerima_souvenir', 'jabatan_penerima_souvenir' )

class PermintaanProtokolerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermintaanProtokoler
        fields = ('id','deskripsi_kebutuhan','status_permintaan_protokoler','alasan_penolakan','created_at','updated_at')

class PerizinanKegiatanSerializer(serializers.ModelSerializer): # untuk post permintaan protokoler dan permintaan souvenir oleh mahasiswa
    permintaan_protokoler = PermintaanProtokolerSerializer(required = False)
    permintaan_souvenir = PermintaanSouvenirSerializer(many=True, required= False)
    
    class Meta:
        model = IzinKegiatan
        fields = ('id', 'permintaan_souvenir', 'permintaan_protokoler')
    
    def update(self, izin_kegiatan, validated_data):
        #protokoler
        if 'permintaan_protokoler' in validated_data:
            permintaan_protokoler= validated_data.pop('permintaan_protokoler')
            PermintaanProtokoler.objects.create(izin_kegiatan=izin_kegiatan, **permintaan_protokoler)

        # souvenir
        if 'permintaan_souvenir' in validated_data:
            permintaan_souvenir_data = validated_data.pop('permintaan_souvenir')
            for permintaan_souvenir in permintaan_souvenir_data:
                PermintaanSouvenir.objects.create(izin_kegiatan=izin_kegiatan, **permintaan_souvenir)
        
        return izin_kegiatan    

class SouvenirSerializerSimpliest(serializers.ModelSerializer):
    class Meta:
        model = Souvenir
        fields = ('stok', 'stok_minimum')

class PerizinKegiatanHumasSerializer(serializers.ModelSerializer): # untuk list izin kegiatan (publikasi, protokoler, souvenir) oleh admin humas
    user = UserSerializer()
    perizinan_publikasi = PerizinanPublikasiHumasSerializer(required=False)
    permintaan_protokoler = PermintaanProtokolerSerializer(required = False)
    permintaan_souvenir =PermintaanSouvenirHumasSerializer(many=True, required= False)

    class Meta:
        model = IzinKegiatan
        fields = ('id','nama_kegiatan', 'organisasi', 'status_perizinan_kegiatan', 'user','perizinan_publikasi','permintaan_souvenir', 'permintaan_protokoler')

