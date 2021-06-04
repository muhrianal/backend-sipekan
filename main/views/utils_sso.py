from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models.profile import Profile


def process_sso_profile(sso_profile):
    try:
        user = User.objects.get(username=sso_profile['username'])
        token, _ = Token.objects.get_or_create(user=user)
        profile = Profile.objects.get(user=user)
    except User.DoesNotExist:
        user = User(username=sso_profile['username'])
        user.set_unusable_password()
        user.save()
        profile = generate_user_profile(user, sso_profile)
        token = Token.objects.create(user=user)
    return token.key, profile, user


def generate_user_profile(user, sso_profile):
    attr = sso_profile['attributes']
    return Profile.objects.create(
        user=user,
        nama=attr['ldap_cn'],
        role = 'MAHASISWA'
    )

