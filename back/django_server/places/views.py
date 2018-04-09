from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from places.models import ProtoPlace, ImageAttach
from places.serializers import SimplePlaceSerializer, InfoPlaceSerializer, ImageSerializer, ProtoPlaceSerializer


class ProtoPlaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProtoPlace.objects.all()
    serializer_class = ProtoPlaceSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageAttach.objects.all()
    serializer_class = ImageSerializer


class TagsPlaceView(generics.RetrieveAPIView):
    lookup_field = 'event_id'
    queryset = ProtoPlace.objects.all()
    serializer_class = SimplePlaceSerializer


class InfoPlaceView(generics.RetrieveAPIView):
    lookup_field = 'event_id'
    queryset = ProtoPlace.objects.all()
    serializer_class = InfoPlaceSerializer


@api_view(['GET'])
@csrf_exempt
def get_places_list(request):
    ids = request.query_params['ids'].split(',')
    ids = [int(id) for id in ids]
    ser = InfoPlaceSerializer()
    places = [ser.to_representation(ProtoPlace.objects.get(event_id=id)) for id in ids]
    return Response(places)

