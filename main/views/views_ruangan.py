from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate

from ..models.profile import Profile
from django.contrib.auth.models import User


from rest_framework import status, permissions
from rest_framework.parsers import JSONParser 
from ..models.peminjaman_ruangan import Ruangan
from django.contrib.auth.models import User

from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from ..permissions import AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM

from ..models.peminjaman_ruangan import Ruangan

from ..serializers.ruangan_serializer import RuanganSerializer
from ..serializers.peminjaman_ruangan_serializer import RuanganSerializer

from django.http.response import JsonResponse

@api_view(['GET'])
@permission_classes([permissions.AllowAny,])
def list_ruangan(request):

    if request.method == 'GET':
        list_ruangan = Ruangan.objects.all()
        ruangan_serialized = RuanganSerializer(list_ruangan, many=True)
        return JsonResponse(ruangan_serialized.data, safe=False)
    
    #case for else
    data = {
        'message' : 'invalid API call'
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)






