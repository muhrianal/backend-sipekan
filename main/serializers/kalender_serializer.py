from rest_framework import serializers 

from ..models.peminjaman_ruangan import PeminjamanRuangan
from . import ruangan_serializer

class KalenderSerializer(serializers.ModelSerializer):

    ruangan = ruangan_serializer.RuanganSerializer()

    class Meta:
        model = PeminjamanRuangan
        fields = ('judul_peminjaman', 'ruangan', 'waktu_mulai', 'waktu_akhir')