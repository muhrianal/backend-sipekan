from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect

from ..sso.decorators import with_sso_ui
from .utils_sso import process_sso_profile
from django.conf import settings


@with_sso_ui(force_login=True)
def login_with_sso(request, sso_profile):

    if sso_profile is not None:

        token, profile, user = process_sso_profile(sso_profile)
        print('ini sso profile: ')

        print(sso_profile)
        data = {
            'username' : user.username,
            'token' : token,
            'id_user': user.pk,
            'role' : profile.role,
            'name' : profile.nama,
            'next_page': 'http://localhost:8081/',
            'cors_origin_whitelist': settings.CORS_ALLOWED_ORIGINS,
        }

        print(data)
        return render(request, 'after-login-sso.html', context=data)
    return redirect(to='/404')
