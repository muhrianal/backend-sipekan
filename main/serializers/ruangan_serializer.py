from rest_framework import serializers 

from ..models.peminjaman_ruangan import Ruangan

class RuanganSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ruangan
        fields = ['id', 'nama']