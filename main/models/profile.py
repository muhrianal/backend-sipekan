from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      nama = models.CharField(max_length=100)

      USER_ROLE_CHOICES = (
        ('MAHASISWA', 'MAHASISWA'),
        ('ADMIN PKM', 'ADMIN PKM'),
        ('ADMIN FASTUR', 'ADMIN FASTUR'),
        ('ADMIN HUMAS', 'ADMIN HUMAS'),
        ('UNIT KERJA', 'UNIT KERJA')
      )

      role = models.CharField(choices=USER_ROLE_CHOICES, max_length=30)

      class Meta:
          app_label = 'main'
