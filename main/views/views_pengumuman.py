from rest_framework.decorators import api_view, permission_classes, parser_classes
from ..models.pengumuman import Pengumuman
from ..serializers.pengumuman_serializer import PengumumanSerializer
from django.http.response import JsonResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status, permissions
from ..permissions import AllowOnlyAdminFASTUR, AllowOnlyAdminHUMAS, AllowOnlyAdminPKM


@api_view(['GET', ])
@permission_classes([permissions.AllowAny,])
def get_all_pengumuman(request):
    if request.method == 'GET':
        list_pengumuman = Pengumuman.objects.all()
        list_pengumuman_serialized = PengumumanSerializer(list_pengumuman, many=True)
        return Response(list_pengumuman_serialized.data)
    return Response({'message': 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET',])
@permission_classes([AllowOnlyAdminFASTUR | AllowOnlyAdminHUMAS | AllowOnlyAdminPKM])
def get_pengumuman_by_id(request, id_pengumuman):
    try:
        pengumuman = Pengumuman.objects.get(pk=id_pengumuman)
    except:
        return JsonResponse({'message': 'Pengumuman tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        pengumuman_serialized = PengumumanSerializer(pengumuman)
        return Response(pengumuman_serialized.data, headers={'Content-Disposition': 'attachment'})
    return JsonResponse({'message': 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)





@api_view(['POST', ])
@parser_classes([MultiPartParser, ])
@permission_classes([AllowOnlyAdminFASTUR | AllowOnlyAdminHUMAS | AllowOnlyAdminPKM])
def post_new_pengumuman(request):
    if request.method == 'POST':
        pengumuman_data_serialized = PengumumanSerializer(data=request.data)
        if pengumuman_data_serialized.is_valid():
            pengumuman_data_serialized.save()
            return JsonResponse(pengumuman_data_serialized.data,status=status.HTTP_201_CREATED,safe=False)
        return JsonResponse(pengumuman_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message': 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT', ])
@parser_classes([MultiPartParser, ])
@permission_classes([AllowOnlyAdminFASTUR | AllowOnlyAdminHUMAS | AllowOnlyAdminPKM])
def put_pengumuman(request, id_pengumuman):
    try:
        pengumuman = Pengumuman.objects.get(pk=id_pengumuman)
    except:
        return JsonResponse({'message': 'Pengumuman tidak ada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        pengumuman_data_serialized = PengumumanSerializer(pengumuman, data=request.data)
        if pengumuman_data_serialized.is_valid():
            pengumuman_data_serialized.save()
            return JsonResponse(pengumuman_data_serialized.data)
        return JsonResponse(pengumuman_data_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message': 'invalid API method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
