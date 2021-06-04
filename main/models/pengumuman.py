from django.db import models

class Pengumuman(models.Model):
    nama = models.CharField(max_length=600)
    deskripsi = models.TextField()
    file_pengumuman = models.FileField(upload_to='file_pengumuman', blank=True, null=True)