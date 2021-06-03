from django.urls import path
from .views.auth import login, test_api_unrestricted
from .views.auth_sso import login_with_sso

from .views.views_peminjaman_ruangan import list_peminjaman_ruangan
from .views.views_izin_kegiatan import list_izin_kegiatan, update_izin_kegiatan_by_id_perizinan, detail_izin_kegiatan

from .views.views_peminjaman_ruangan import list_jadwal
from .views.views_ruangan import list_ruangan
from .views.views_peminjaman_ruangan import list_ruangan
from .views.views_peminjaman_ruangan import detail_ruangan
from .views.views_status_perizinan import list_perizinan, detail_perizinan
from .views.views_peminjaman_ruangan import post_peminjaman_ruangan_mahasiswa
from .views.views_humas import get_post_perizinan_humas,list_perizinan_humas, get_jenis_publikasi, get_list_souvenir, post_perizinan_publikasi
from .views.views_izin_kegiatan_mahasiswa import get_post_izin_kegiatan_mahasiswa, post_izin_kegiatan_detail, post_izin_kegiatan_header
from .views.views_peminjaman_ruangan import update_peminjaman_ruangan_by_id_peminjaman_ruangan, post_peminjaman_ruangan_unit_kerja, get_list_perizinan_fastur, get_peminjaman_ruangan_by_id_izin_kegiatan
from .views.views_pengumuman import get_all_pengumuman, post_new_pengumuman, get_pengumuman_by_id, put_pengumuman

urlpatterns = [
    path('login/', login),
    path('test-api/', test_api_unrestricted),
    path('login-sso/', login_with_sso),
    path('list-peminjaman-ruangan/', list_peminjaman_ruangan),
    path('izin-kegiatan/update/<int:id_perizinan>/', update_izin_kegiatan_by_id_perizinan),
    path('izin-kegiatan/', list_izin_kegiatan),
    path('izin-kegiatan/<int:pk>', detail_izin_kegiatan),
    path('api/ruangan/', list_ruangan),
    path('api/ruangan/<int:pk>/', detail_ruangan),
    path('api/list-perizinan/', list_perizinan),
    path('api/perizinan/<int:pk>', detail_perizinan),
    path('peminjaman-ruangan/update/<int:id_peminjaman>/', update_peminjaman_ruangan_by_id_peminjaman_ruangan),
    path('peminjaman-ruangan/mahasiswa/<int:id_izin_kegiatan>/', post_peminjaman_ruangan_mahasiswa),
    path('perizinan-humas/<int:id_izin_kegiatan>/',get_post_perizinan_humas),
    path('perizinan-humas-publikasi/',post_perizinan_publikasi),
    path('list-perizinan-humas/',list_perizinan_humas),
    path('perizinan-kegiatan-mahasiswa/',get_post_izin_kegiatan_mahasiswa),
    path('perizinan-kegiatan-header/',post_izin_kegiatan_header),
    path('perizinan-kegiatan-detail/',post_izin_kegiatan_detail),
    path('perizinan-humas/jenis-publikasi', get_jenis_publikasi),
    path('perizinan-humas/list-souvenir', get_list_souvenir),
    path('peminjaman-ruangan/', list_jadwal),
    path('peminjaman-ruangan/update-status/<int:id_peminjaman>/', update_peminjaman_ruangan_by_id_peminjaman_ruangan),
    path('peminjaman-ruangan/unit-kerja/', post_peminjaman_ruangan_unit_kerja),
    path('peminjaman-ruangan/verifikasi-fastur/', get_list_perizinan_fastur),
    path('peminjaman-ruangan/verifikasi-fastur/<int:id_izin_kegiatan>/', get_peminjaman_ruangan_by_id_izin_kegiatan),   
    path('pengumuman/', get_all_pengumuman),
    path('pengumuman/create', post_new_pengumuman),
    path('pengumuman/<int:id_pengumuman>', get_pengumuman_by_id),
    path('pengumuman/edit/<int:id_pengumuman>', put_pengumuman),
]
