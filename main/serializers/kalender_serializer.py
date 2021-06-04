from rest_framework import serializers 

from ..models.peminjaman_ruangan import PeminjamanRuangan
from . import ruangan_serializer
from . import peminjaman_ruangan_serializer

class KalenderSerializer(serializers.ModelSerializer):

    ruangan = ruangan_serializer.RuanganSerializer()
    perulangan = peminjaman_ruangan_serializer.PerulanganSerializer()

    class Meta:
        model = PeminjamanRuangan
        fields = ('judul_peminjaman', 'ruangan', 'perulangan', 'waktu_mulai', 'waktu_akhir')
