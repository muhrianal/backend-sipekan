from django.contrib import admin

from .models.profile import Profile
from .models.izin_kegiatan import IzinKegiatan, DetailKegiatan
from .models.pengumuman import Pengumuman

from .models.peminjaman_ruangan import PeminjamanRuangan, Ruangan, Perulangan
from .models.humas import PerizinanPublikasi, PermintaanProtokoler, PermintaanSouvenir, Souvenir, JenisPublikasi, JenisIzinPublikasi

# Register your models here.
admin.site.register(Profile)

admin.site.register(PeminjamanRuangan)
admin.site.register(Ruangan)


admin.site.register(IzinKegiatan)

admin.site.register(DetailKegiatan)


admin.site.register(PerizinanPublikasi)

admin.site.register(PermintaanProtokoler)

admin.site.register(PermintaanSouvenir)

admin.site.register(Perulangan)

admin.site.register(Souvenir)
admin.site.register(JenisPublikasi)
admin.site.register(JenisIzinPublikasi)

admin.site.register(Pengumuman)
