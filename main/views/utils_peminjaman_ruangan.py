from ..models.peminjaman_ruangan import PeminjamanRuangan, Perulangan
import datetime
from django.utils import timezone

SEKALI_PAKAI = 1
HARIAN = 2
MINGGUAN = 3
BULANAN = 4

def is_available(izin_kegiatan_data):

    list_booked_peminjaman = PeminjamanRuangan.objects.exclude(perulangan__tanggal_akhir__lt=datetime.date.today())
    list_peminjaman_diajukan = izin_kegiatan_data['peminjaman_ruangan']

    print(list_peminjaman_diajukan)

    for peminjaman_diajukan in list_peminjaman_diajukan:
        if int(peminjaman_diajukan["perulangan"]["jenjang"]) == SEKALI_PAKAI:
            print("masuk if pertama")
            if check_sekali_pakai(peminjaman_diajukan, list_booked_peminjaman):
                print("masuk if kedua")
                return False
        if int(peminjaman_diajukan["perulangan"]["jenjang"]) == HARIAN:
            print('masuk if harian')
            if check_harian(peminjaman_diajukan, list_booked_peminjaman):
                return False
        if int(peminjaman_diajukan["perulangan"]["jenjang"]) == MINGGUAN:
            if check_mingguan(peminjaman_diajukan, list_booked_peminjaman):
                return False
        if int(peminjaman_diajukan["perulangan"]["jenjang"]) == BULANAN:
            if check_bulanan(peminjaman_diajukan, list_booked_peminjaman):
                return False
    return True


def check_sekali_pakai(peminjaman_diajukan,list_booked_peminjaman):
    list_booked_peminjaman_by_ruangan = list_booked_peminjaman.filter(ruangan__id=peminjaman_diajukan['ruangan'])


    
    for peminjaman in list_booked_peminjaman_by_ruangan:
        print(peminjaman)
        if int(peminjaman.perulangan.jenjang) == SEKALI_PAKAI:
            print("masuk if pertama again")
            if is_clash(peminjaman_diajukan, peminjaman):
                print("masuk if kedua again")
                return True
        if int(peminjaman.perulangan.jenjang) == HARIAN:
            while(peminjaman.perulangan.tanggal_mulai <= peminjaman.perulangan.tanggal_akhir):
                print("masuk sini")
                if is_clash(peminjaman_diajukan, peminjaman):
                    return True
                peminjaman.perulangan.tanggal_mulai += datetime.timedelta(days=1)
        if int(peminjaman.perulangan.jenjang) == MINGGUAN:
            while(peminjaman.perulangan.tanggal_mulai <= peminjaman.perulangan.tanggal_akhir):
                if is_clash(peminjaman_diajukan, peminjaman):
                    return True
                peminjaman.perulangan.tanggal_mulai += datetime.timedelta(days=7)
        if int(peminjaman.perulangan.jenjang) == BULANAN:
            while(peminjaman.perulangan.tanggal_mulai <= peminjaman.perulangan.tanggal_akhir):
                if is_clash(peminjaman_diajukan, peminjaman):
                    return True
                try:
                    peminjaman.perulangan.tanggal_mulai = peminjaman.perulangan.tanggal_mulai.replace(month=peminjaman.perulangan.tanggal_mulai.month+1)
                except ValueError:
                    if peminjaman.perulangan.tanggal_mulai.month == 12:
                        peminjaman.perulangan.tanggal_mulai = peminjaman.perulangan.tanggal_mulai.replace(year=peminjaman.perulangan.tanggal_mulai.year+1, month=1)
                    else: continue
    print("return False")
    return False



def check_harian(peminjaman_diajukan,list_booked_peminjaman):
    print('ini list: ', list_booked_peminjaman)
    
    tanggal_mulai = datetime.date.fromisoformat(peminjaman_diajukan["perulangan"]["tanggal_mulai"])
    tanggal_akhir = datetime.date.fromisoformat(peminjaman_diajukan["perulangan"]["tanggal_akhir"])
    while tanggal_mulai < tanggal_akhir:
        temp_dict = {
            'ruangan': peminjaman_diajukan['ruangan'],
            'waktu_mulai': peminjaman_diajukan["waktu_mulai"],
            'waktu_akhir' : peminjaman_diajukan["waktu_akhir"],
            'perulangan' : {'jenjang': SEKALI_PAKAI, 'tanggal_mulai' : str(tanggal_mulai), 'tanggal_akhir': str(tanggal_mulai)},

        }
        if check_sekali_pakai(temp_dict, list_booked_peminjaman):
            return True
        print(tanggal_mulai)
        tanggal_mulai += datetime.timedelta(days=1)
    
    return False

def check_mingguan(peminjaman_diajukan,list_booked_peminjaman):
    tanggal_mulai = datetime.date.fromisoformat(peminjaman_diajukan["perulangan"]["tanggal_mulai"])
    tanggal_akhir = datetime.date.fromisoformat(peminjaman_diajukan["perulangan"]["tanggal_akhir"])
    while tanggal_mulai < tanggal_akhir:
        temp_dict = {
            'ruangan': peminjaman_diajukan['ruangan'],
            'waktu_mulai': peminjaman_diajukan["waktu_mulai"],
            'waktu_akhir' : peminjaman_diajukan["waktu_akhir"],
            'perulangan' : {'jenjang': SEKALI_PAKAI, 'tanggal_mulai' : str(tanggal_mulai), 'tanggal_akhir': str(tanggal_mulai)},

        }
        if check_sekali_pakai(temp_dict, list_booked_peminjaman):
            return True
        tanggal_mulai += datetime.timedelta(days=7)
    return False
    
def check_bulanan(peminjaman_diajukan,list_booked_peminjaman):
    tanggal_mulai = datetime.date.fromisoformat(peminjaman_diajukan["perulangan"]["tanggal_mulai"])
    tanggal_akhir = datetime.date.fromisoformat(peminjaman_diajukan["perulangan"]["tanggal_akhir"])
    while tanggal_mulai < tanggal_akhir:
        temp_dict = {
            'ruangan': peminjaman_diajukan['ruangan'],
            'waktu_mulai': peminjaman_diajukan["waktu_mulai"],
            'waktu_akhir' : peminjaman_diajukan["waktu_akhir"],
            'perulangan' : {'jenjang': SEKALI_PAKAI, 'tanggal_mulai' : str(tanggal_mulai), 'tanggal_akhir': str(tanggal_mulai)},

        }
        if check_sekali_pakai(temp_dict, list_booked_peminjaman):
            return True
        
        try:
            tanggal_mulai = tanggal_mulai.replace(month=tanggal_mulai.month+1)
        except ValueError:
            if tanggal_mulai.month == 12:
                tanggal_mulai = tanggal_mulai.replace(year=tanggal_mulai.year+1, month=1)
            else: continue
    
    return False

def is_clash(peminjaman_diajukan, peminjaman):

    
    return helper_is_clash(
                datetime.date.fromisoformat(peminjaman_diajukan["perulangan"]["tanggal_mulai"]) , 
                datetime.datetime.fromisoformat(peminjaman_diajukan["waktu_mulai"]),
                datetime.datetime.fromisoformat(peminjaman_diajukan["waktu_akhir"]),
                peminjaman.perulangan.tanggal_mulai,
                peminjaman.waktu_mulai,
                peminjaman.waktu_akhir
            )


def helper_is_clash(first_tanggal, first_waktu_mulai, first_waktu_akhir, sec_tanggal, sec_waktu_mulai, sec_waktu_akhir):

    sec_waktu_akhir =  timezone.make_naive(sec_waktu_akhir)
    sec_waktu_mulai =  timezone.make_naive(sec_waktu_mulai)

    if first_tanggal != sec_tanggal:
        return False
    
    if (first_waktu_mulai < sec_waktu_mulai and first_waktu_akhir < sec_waktu_mulai) and (first_waktu_mulai < sec_waktu_akhir and first_waktu_akhir < sec_waktu_akhir):
        return False

    if (sec_waktu_mulai < first_waktu_mulai and sec_waktu_akhir < first_waktu_mulai) and (sec_waktu_mulai < first_waktu_akhir and sec_waktu_akhir < first_waktu_akhir):
        return False
    return True
