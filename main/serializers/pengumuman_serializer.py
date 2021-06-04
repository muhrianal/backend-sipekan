from rest_framework import serializers 
from ..models.pengumuman import Pengumuman

class PengumumanSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        file_pengumuman = data.get('file_pengumuman')

        return_data = {
            'nama' : data.get('nama'),
            'deksripsi' : data.get('deskripsi')
        }

        if isinstance(file_pengumuman, str):
            if file_pengumuman == 'null':
                return_data['file_pengumuman'] = None
            else: return return_data
        else:
            return_data['file_pengumuman'] = file_pengumuman
        
        return return_data
            


    class Meta:
        model = Pengumuman
        fields = ['nama', 'deskripsi', 'file_pengumuman']

 