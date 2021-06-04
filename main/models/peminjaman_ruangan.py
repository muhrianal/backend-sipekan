from django.db import models
from django.contrib.auth.models import User
from ..models.izin_kegiatan import IzinKegiatan
from django.utils import timezone

class Ruangan(models.Model):
    JENIS_RUANG_CHOICES = (
      (1, 'Ruang Pertemuan'),
      (2, 'Ruang Kelas'),
      (3, 'Ruang Rapat'),
      (4, 'Selasar'),
    )

    jenis_ruang = models.PositiveSmallIntegerField(choices=JENIS_RUANG_CHOICES, default=-1)
    nama = models.CharField(max_length=255)
    kapasitas = models.IntegerField()
    lokasi = models.CharField(max_length=255)
    fasilitas = models.CharField(max_length=255, default=None, blank=True, null=True)
    waktu_available_mulai = models.DateTimeField(blank=True, null=True)
    waktu_available_akhir = models.DateTimeField(blank=True, null=True)
    informasi_tambahan = models.CharField(max_length=255, default=None, blank=True, null=True)
    STATUS_RUANG_CHOICES = (
       (1, 'Aktif'),
       (2, 'Nonaktif'),
    )
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS_RUANG_CHOICES, blank=True, null=True )


    class Meta:
        app_label = 'main'


class PeminjamanRuangan(models.Model):
    judul_peminjaman = models.CharField(max_length=255)
    izin_kegiatan = models.ForeignKey(
        IzinKegiatan, related_name='peminjaman_ruangan',
        on_delete=models.CASCADE

    )

    jumlah_peserta = models.BigIntegerField(default=0)

    STATUS_CHOICES = (
      (1, 'Menunggu Persetujuan'),
      (2, 'Disetujui'),
      (3, 'Ditolak'),
    )

    status_peminjaman_ruangan = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    alasan_penolakan = models.CharField(max_length=500, default=None, blank=True, null=True)
    ruangan = models.ForeignKey(
        Ruangan,
        on_delete=models.CASCADE
    )
    waktu_mulai = models.DateTimeField()
    waktu_akhir = models.DateTimeField()
    catatan = models.CharField(max_length=500, default=None, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    terbuka_untuk_umum = models.BooleanField(default=False)

    class Meta:
        app_label = 'main'


class Perulangan(models.Model):
    peminjaman_ruangan = models.OneToOneField(PeminjamanRuangan, on_delete=models.CASCADE)

    JENJANG_CHOICES = (
      (1, 'SEKALI PAKAI'),
      (2, 'HARIAN'),
      (3, 'MINGGUAN'),
      (4, 'BULANAN'),
    )

    jenjang = models.PositiveSmallIntegerField(choices=JENJANG_CHOICES)
    tanggal_mulai = models.DateField()
    tanggal_akhir = models.DateField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    

    class Meta:
        app_label = 'main'