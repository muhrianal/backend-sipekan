from django.urls import path
from .views.auth import login, test_api_unrestricted
from .views.auth_sso import login_with_sso

from .views.views_peminjaman_ruangan import list_peminjaman_ruangan
from .views.views_izin_kegiatan import list_izin_kegiatan, update_izin_kegiatan_by_id_perizinan, detail_izin_kegiatan, get_list_perizinan_PKM, get_list_perizinan_PKM_Verified, get_list_perizinan_PKM_Waiting_Simplified, get_list_perizinan_PKM_Verified_Simplified, get_list_perizinan_PKM_Denied_Simplified, get_list_perizinan_Humas_Waiting_Simplified, get_list_souvenir_simple

from .views.views_peminjaman_ruangan import list_jadwal
from .views.views_ruangan import list_ruangan
from .views.views_peminjaman_ruangan import list_ruangan
from .views.views_peminjaman_ruangan import detail_ruangan
from .views.views_status_perizinan import list_perizinan, detail_perizinan, list_perizinan_detailed
from .views.views_peminjaman_ruangan import post_peminjaman_ruangan_mahasiswa
from .views.views_humas import get_post_perizinan_humas_by_id_izin_kegiatan, get_jenis_publikasi, get_list_souvenir, post_perizinan_publikasi, post_souvenir, detail_souvenir, detail_permintaan_protokoler, detail_permintaan_souvenir
from .views.views_izin_kegiatan_mahasiswa import  post_izin_kegiatan_detail, post_izin_kegiatan_header, put_izin_kegiatan_header, put_izin_kegiatan_detail
from .views.views_peminjaman_ruangan import update_peminjaman_ruangan_by_id_peminjaman_ruangan, post_peminjaman_ruangan_unit_kerja, get_list_perizinan_fastur, get_peminjaman_ruangan_by_id_izin_kegiatan, detail_peminjaman_ruangan, perulangan
from .views.views_humas import get_post_perizinan_humas_by_id_izin_kegiatan,get_list_perizinan_humas, get_jenis_publikasi, get_list_souvenir, post_perizinan_publikasi, update_permintaan_souvenir_by_id_permintaan_souvenir,  update_permintaan_protokoler_by_id_permintaan_protokoler, update_jenis_izin_publikasi_by_id_jenis_izin_publikasi, put_perizinan_publikasi
from .views.views_izin_kegiatan_mahasiswa import post_izin_kegiatan_detail, post_izin_kegiatan_header
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
    path('perizinan-humas/<int:id_izin_kegiatan>/',get_post_perizinan_humas_by_id_izin_kegiatan),
    path('perizinan-humas-publikasi/',post_perizinan_publikasi),
    path('perizinan-humas/verifikasi-humas/',get_list_perizinan_humas),
    path('perizinan-humas/verifikasi-humas/<int:id_izin_kegiatan>/',get_post_perizinan_humas_by_id_izin_kegiatan),
    path('perizinan-humas/update-status-souvenir/<int:id_permintaan>/',update_permintaan_souvenir_by_id_permintaan_souvenir),
    path('perizinan-humas/update-status-protokoler/<int:id_permintaan>/',update_permintaan_protokoler_by_id_permintaan_protokoler),
    path('perizinan-humas/update-status-jenis-izin-publikasi/<int:id_jenis_izin_publikasi>/',update_jenis_izin_publikasi_by_id_jenis_izin_publikasi),
    path('perizinan-kegiatan-header/',post_izin_kegiatan_header),
    path('perizinan-kegiatan-detail/',post_izin_kegiatan_detail),
    path('perizinan-humas/jenis-publikasi', get_jenis_publikasi),
    path('perizinan-humas/list-souvenir', get_list_souvenir),
    path('peminjaman-ruangan/', list_jadwal),
    path('peminjaman-ruangan/update-status/<int:id_peminjaman>/', update_peminjaman_ruangan_by_id_peminjaman_ruangan),
    path('peminjaman-ruangan/unit-kerja/', post_peminjaman_ruangan_unit_kerja),
    path('peminjaman-ruangan/verifikasi-fastur/', get_list_perizinan_fastur),
    path('peminjaman-ruangan/verifikasi-fastur/<int:id_izin_kegiatan>/', get_peminjaman_ruangan_by_id_izin_kegiatan),
    path('izin-kegiatan-waiting/', get_list_perizinan_PKM),  
    path('izin-kegiatan-disetujui/', get_list_perizinan_PKM_Verified),
    path('izin-kegiatan-detailed/', list_perizinan_detailed),
    path('chart/kegiatan-disetujui/', get_list_perizinan_PKM_Verified_Simplified),
    path('chart/kegiatan-ditolak/', get_list_perizinan_PKM_Denied_Simplified),
    path('chart/kegiatan-menunggu/', get_list_perizinan_PKM_Waiting_Simplified),
    path('perizinan-humas-disetujui/', get_list_perizinan_Humas_Waiting_Simplified),
    path('stok-souvenir/', get_list_souvenir_simple),
    path('souvenir/', post_souvenir),
    path('souvenir/<int:pk>/', detail_souvenir),
    path('permintaan-protokoler/<int:pk>/', detail_permintaan_protokoler),
    path('permintaan-souvenir/<int:pk>/', detail_permintaan_souvenir),
    path('peminjaman-ruangan/<int:pk>/', detail_peminjaman_ruangan),
    path('detail-kegiatan/<int:pk>/', put_izin_kegiatan_header),
    path('izin-kegiatan-detail/<int:pk>/', put_izin_kegiatan_detail),
    path('perulangan/<int:pk>/', perulangan),
    path('perizinan-publikasi/<int:pk>', put_perizinan_publikasi),
    path('peminjaman-ruangan/verifikasi-fastur/<int:id_izin_kegiatan>/', get_peminjaman_ruangan_by_id_izin_kegiatan),   
    path('pengumuman/', get_all_pengumuman),
    path('pengumuman/create', post_new_pengumuman),
    path('pengumuman/<int:id_pengumuman>', get_pengumuman_by_id),
    path('pengumuman/edit/<int:id_pengumuman>', put_pengumuman),
]
