from django.db import models
from django.contrib.auth.models import User
# from ..models.peminjaman_ruangan import PeminjamanRuangan
# from ..models.humas import PermintaanProtokoler, PerizinanPublikasi, PermintaanSouvenir

from django.utils import timezone
class IzinKegiatan(models.Model):
    nama_kegiatan = models.CharField(max_length=255)
    organisasi = models.CharField(max_length=255)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    STATUS_CHOICES = (
      (1, 'Menunggu Persetujuan'),
      (2, 'Disetujui'),
      (3, 'Ditolak'),
    )

    status_perizinan_kegiatan = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)

    class Meta:
        app_label = 'main'


class DetailKegiatan(models.Model):
    izin_kegiatan = models.OneToOneField(
        IzinKegiatan,
        on_delete=models.CASCADE,
        related_name="detail_kegiatan"
        
    )

    waktu_tanggal_mulai = models.DateTimeField()
    waktu_tanggal_akhir = models.DateTimeField()
    email_pic = models.EmailField()
    nama_pic = models.CharField(max_length=255)
    hp_pic = models.CharField(max_length=255)
    npm_pic = models.CharField(max_length=255)
    npm_ketua_organisasi = models.CharField(max_length=255)
    nama_ketua_organisasi = models.CharField(max_length=255)
    tempat_pelaksanaan = models.CharField(max_length=255)
    sumber_pendanaan = models.CharField(max_length=255)
    alasan_penolakan = models.CharField(max_length=500, default=None, blank=True, null=True)
    file_info_kegiatan = models.FileField(upload_to='file_kegiatan',default=None, null=True,blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        app_label = 'main'