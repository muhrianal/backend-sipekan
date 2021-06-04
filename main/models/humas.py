from django.db import models
from django.contrib.auth.models import User
from .izin_kegiatan import IzinKegiatan

from django.utils import timezone

class PermintaanProtokoler(models.Model):
    izin_kegiatan = models.OneToOneField(
        IzinKegiatan,
        related_name = 'permintaan_protokoler',
        on_delete=models.CASCADE
    )

    deskripsi_kebutuhan = models.CharField(max_length=500)
    alasan_penolakan = models.CharField(max_length=500, default=None, blank=True, null=True)
    STATUS_CHOICES = (
      (1, 'Menunggu Persetujuan'),
      (2, 'Disetujui'),
      (3, 'Ditolak'),
    )
    status_permintaan_protokoler = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'main'

class JenisPublikasi(models.Model):
    luar_ruangan =  models.BooleanField()
    deskripsi_publikasi = models.CharField(max_length=500)

    class Meta:
        app_label = 'main'

class PerizinanPublikasi(models.Model):
    izin_kegiatan = models.OneToOneField(
        IzinKegiatan,
        related_name = 'perizinan_publikasi',
        on_delete=models.CASCADE
    )
    tanggal_mulai = models.DateField()
    tanggal_akhir = models.DateField()

    
    keterangan = models.CharField(max_length=500, default=None, blank=True, null=True)
    file_materi_kegiatan = models.FileField(upload_to='file_materi_kegiatan', blank=True)
    file_flyer_pengumuman = models.FileField(upload_to='file_flyer_pengumuman',blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        app_label = 'main'
    
class JenisIzinPublikasi(models.Model):
    perizinan_publikasi = models.ForeignKey(
        PerizinanPublikasi,
        related_name = 'jenis_izin_publikasi',
        on_delete=models.CASCADE
    )
    
    jenis_publikasi = models.ForeignKey(
        JenisPublikasi,
        on_delete = models.CASCADE
    )
    
    STATUS_CHOICES = (
      (1, 'Menunggu Persetujuan'),
      (2, 'Disetujui'),
      (3, 'Ditolak'),
    )

    status_perizinan_publikasi = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    alasan_penolakan = models.CharField(max_length=500, default=None, blank=True, null=True)

class Souvenir(models.Model):
    nama_souvenir = models.CharField(max_length=255)
    
    KELAS_CHOICES = (
        (1, 'Kelas 1'),
        (2, 'Kelas 2'),
        (3, 'Kelas 3'),
        (4, 'Kelas 1 & Kelas 2'),
        (5, 'Kelas 1 & Kelas 3'),
        (6, 'Kelas 2 & Kelas 3'),
        (7, 'Kelas 1 & Kelas 2 & Kelas 3'),
    )

    kelas = models.PositiveSmallIntegerField(choices=KELAS_CHOICES)

    REGION_CHOICES = (
        (1, 'Dalam Negeri'),
        (2, 'Luar Negeri'),
        (3, 'Dalam dan Luar Negeri'),
    )
    region = models.PositiveSmallIntegerField(choices=REGION_CHOICES)
    
    stok = models.IntegerField()
    stok_minimum = models.IntegerField(default=1)
    tanggal_masuk = models.DateField(default=None, blank=True, null=True)
    keterangan = models.CharField(max_length=500, default=None, blank=True, null=True)

    class Meta:
        app_label = 'main'


class PermintaanSouvenir(models.Model):
    izin_kegiatan = models.ForeignKey(
        IzinKegiatan,
        related_name = 'permintaan_souvenir',
        on_delete=models.CASCADE
    )
    alasan_penolakan = models.CharField(max_length=500, default=None, blank=True, null=True)
    
    STATUS_CHOICES = (
      (1, 'Menunggu Persetujuan'),
      (2, 'Disetujui'),
      (3, 'Ditolak'),
    )

    status_permintaan_souvenir = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    jumlah = models.IntegerField()
    souvenir = models.ForeignKey(
        Souvenir,
        on_delete=models.CASCADE,
    )
    nama_penerima_souvenir = models.CharField(max_length=255)
    jabatan_penerima_souvenir = models.CharField(max_length=255)
    
    KELAS_CHOICES = (
        (1, 'Kelas 1'),
        (2, 'Kelas 2'),
        (3, 'Kelas 3'),
    )
    
    kelas_penerima_souvenir = models.PositiveSmallIntegerField(choices=KELAS_CHOICES)

    REGION_CHOICES = (
        (1, 'Dalam Negeri'),
        (2, 'Luar Negeri'),
        (3, 'Dalam dan Luar Negeri'),
    )
    region_penerima_souvenir = models.PositiveSmallIntegerField(choices=KELAS_CHOICES)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        app_label = 'main'