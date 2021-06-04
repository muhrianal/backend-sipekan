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


@api_view(['POST',])
@permission_classes([permissions.AllowAny,])
def login(request):
    
    login_data = JSONParser().parse(request)

    username = login_data['username']
    password = login_data['password']

    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        

        return_data = {
            'username' : username,
            'token' : str(token),
            'id_user' : user.pk
        }
        try:
            profile = Profile.objects.get(user=user)

            if profile is not None:
                return_data['role'] = profile.role
                return_data['name'] = profile.nama 
        except:
            return Response(data=return_data, status=status.HTTP_200_OK)
    
        return Response(data=return_data, status=status.HTTP_200_OK)
    
    data = {'message': 'login gagal'}
    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET','POST'])
@permission_classes((permissions.AllowAny,))
def test_api_unrestricted(request):
    """
    Contoh API sederhana. By default semua API itu di restriksi, jadi harus pake header dengan tokennya (harus udh login).
    Jadi, kalo mau bikin API yg gak harus pake token, seperti login misalnya, maka harus tambahin decorator: @permission_classes((permissions.AllowAny,))
    di atas function nya.
    """

    print("role dari request: ", end=" ")
    user = request.user
    # print(request.user)
    profile = Profile.objects.get(user=user)

    print(profile.role)
    data = {
        'message' : 'API berhasil di call',
    }

    return Response(data=data, status=status.HTTP_200_OK)

