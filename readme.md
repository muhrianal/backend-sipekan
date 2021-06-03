
# Backend SIPEKAN w/ **Django**


## Persiapan

1. Clone Repository ini dengan:

```
git clone https://github.com/muhrianal/sipekan.git
```

2. Install dan buat virtual environment python (kalau lupa bisa cari di Internet, disini tidak dicantumkan karena tiap OS beda caranya)
3. Jangan lupa aktifkan virtual environment-nya
4. Install dependencies-nya

```
pip install -r requirements.txt
```

4. Django app sudah bisa dijalankan

Sebelumnya, jalankan dulu perintah berintah berikut:
```
python manage.py makemigrations
python manage.py migrate
```

perintah di atas harus dijalankan setiap terjadi perubahan di model, admin, dll

untuk menjalankan aplikasi
```
python manage.py runserver
```

## Tentang GIT

* Buat terlebih dahulu branch masing-masing
```
git branch dev/{nama_kalian}
```

Setelah menjalankan perintah diatas, kamu baru membuat branch namun belum berpindah ke branch tersebut

* Pindah ke branch yang telah kalian buat
```
git checkout dev/{nama_kalian}
```

Cara lain untuk membuat branch sekaligus langsung berpindah ke branch tersebut:
```
git checkout -b dev/{nama_kalian}
```

#### Untuk ngepush:

* Cek dulu udah di branch masing-masing atau belum 
```
git status
```

Kalo branch-nya masih belum di branch masing-masing, pindah dulu yaaa pake cara sebelumnya.

Kalo udh di branch:
```
git add .
git commit -m "jelasin disini tujuan ngepushnya apa (misal apa yang diubah)"
git push origin dev/{nama_kalian}
```

Perhatikan bahwa saat jalanin git add itu diakhiri dengan titik yang artinya ngepush semua yang telah diubah. Kalo misal mau ngepush salah satu file doang bisa diganti jadi:
```
git add directory/to/the/file
```

#### **Note: jangan pernah ngepush ke master!**

## Tentang Python, Django, dan REST API

1. Silakan buka-buka dulu folder ```main/```.
Disana ada folder models, views, dan file urls.py. Mostly kita akan banyak ngoding disitu untuk keperluan REST API. Cek-cek aja dulu, hehe
2. Untuk membuat endpoint API, buat terlebih dahulu file python (.py) di dalam folder views.
Beri nama yang sesuai dan representatif, misal untuk kebutuhan izin kegiatan bisa beri nama views_izin_kegiatan.py
3. Lalu, bentuk kodingan di views nanti kurang lebih akan sebagai berikut:
```python

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([permissions.AllowAny,])
def izin_kegiatan_api(request):
    if request.method == 'GET':
        #do something untuk request GET. misal nge return list kegiatan atau apa
    elif request.method == 'POST':
        #do something untuk request POST, misal bikin izin kegiatan baru
    elif request.method == 'DELETE':
        #do something untuk request DELETE, misal hapus izin kegiatan yang sudah ada
```

Penjelasan:
* Perlu diperhatikan bahwa di baris pertama ada decorator @api_view([list yang isinya task apa aja yang boleh]). Jadi disini teman-teman definisiin dulu yang boleh tuh apa aja, kalo cuma get doang yang boleh yaudah isi dengan 'GET'.
* Di baris kedua ada decorator @permission_classes([list permission apa aja yang boleh]). Pada dasarnya, setiap API yang gaada decorator seperti ini di-set akan selalu bisa menerima task asalkan user telah login, gak peduli rolenya apa. Tapi, untuk kasus diatas itu kan dia listnya berisi permissions.AllowAny. Kalo seperti itu, artinya endpoint api tersebut bisa di akses oleh siapapun tanpa harus terotentikasi. Ini contoh penggunaannya buat endpoint login, login kan bisa diakses siapapun hehe. 
* Lalu, gue juga udh bikin beberapa custom permission, contohnya misal suatu endpoint API cuma bisa diakses oleh role ADMIN PKM doang. Nah itu tinggal pake custom permission yang udh dibuat. tinggal import:
```python
from ..permissions import AllowOnlyAdminPKM,
```
Silakan dicek aja di file permissions.py, disitu udh ada beberapa custom permission yang siap dipakai.
* Terus gimana kalo misal ada kasus: kalo user role mahasiswa boleh GET tapi kalo user Admin PKM bisa GET, POST, DELETE, PUT? nah itu bisa juga di custom, kalo ada yg punya kebetuhan seperti itu boleh sampein aja ke gue, nanti bisa dibantu.
* Untuk import-import an yang bakal sering dipake
```python

from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate

from ..models.profile import Profile
from django.contrib.auth.models import User

from rest_framework import status, permissions
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


```

4. Setelah bikin fungsi views seperti diatas, sekarang kita bikin url nya atau endpointnya. Buka file urls.py di dalam folder main.
Disana kurang lebih kodingannya akan seperti ini:

```python
from django.urls import path
from .views.auth import login, test_api_unrestricted
from .views.auth_sso import login_with_sso
urlpatterns = [
    path('login/', login),
    path('test-api/', test_api_unrestricted),
    path('login-sso/', login_with_sso)
]

```
Nah temen-temen tinggal import views yang telah teman-teman buat dan tambahkan kodingan berikut didalam list urlpatterns:
```python
    path('link-nya-mau-kemana/', nama_function_dari_views)
```
5. Selesai deh, API seharusnya sudah bisa berjalan.

In case teman-teman butuh tutorial yang lebih komprehensif : https://bezkoder.com/django-rest-api/