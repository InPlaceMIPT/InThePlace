import cloudinary
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
from images.models import Image
from images.serializers import ImageSerializer
import re

all_tags = ["populous", "alone", "family", "friends", "calm", "active",
            "food", "drinks", "alcohol", "noisy", "quiet", "nature", "city",
            "fragrant", "cinema", "sad", "gloomy",
            "fast", "long", "free", "cheap", "expensive", "culture", "adrenaline"]

groups = [["populous", "alone", "family", "friends"],
          ["food", "drinks", "cinema", "alcohol"],
          ["city", "noisy", "quiet", "nature"],
          ["calm","adrenaline" , "active", "sad"],
          ["gloomy", "fast", "long", "fragrant"],
          ["cheap", "expensive", "free","culture"]]


class ImagePull:

    def __init__(self):
        self.images_by_tag = []
        self.update()

    def get_images_with_tag(self, tag):
        result = []
        try:
            result = list(self.images_by_tag[all_tags.index(tag)])
        finally:
            pass
        return result

    def update(self):
        self.images_by_tag = []
        for tag in all_tags:
            self.images_by_tag.append(set())
        images = Image.objects.all()
        for im in images:
            tags = im.inplace_tags.split(';')
            for tag in tags:
                try:
                    self.images_by_tag[all_tags.index(tag)].add(im.image_id)
                finally:
                    pass


global_image_pull = None


def get_image_pull():
    global global_image_pull
    if not global_image_pull:
        global_image_pull = ImagePull()
    return global_image_pull


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageView(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_field = 'image_id'


@api_view(['GET'])
@csrf_exempt
def get_tags_list(request):
    return Response(all_tags)


def get_images_set_list(group):
    pl = get_image_pull()
    picked = []
    for tag in groups[group]:
        images = pl.get_images_with_tag(tag)
        picked.append(random.choice(images))
    return picked


@api_view(['GET'])
@csrf_exempt
def get_images_set(request):
    group = int(request.query_params['group'])
    return Response({"images": get_images_set_list(group)})


@api_view(['GET'])
@csrf_exempt
def get_images_in_one(request):
    group = int(request.query_params['group'])
    picked = get_images_set_list(group)
    images = [Image.objects.get(image_id=id).image for id in picked]
    url = cloudinary.CloudinaryImage(str(images[0])).build_url(transformation=[
  {"width": 440, "height": 280, "crop": "fill"},
  {"overlay": re.sub(r'/', ':', str(images[1])), "width": 440, "height": 280, "x": 440, "crop": "fill"},
  {"overlay": re.sub(r'/', ':', str(images[2])), "width": 440, "height": 280, "y": 280, "x": -220, "crop": "fill"},
  {"overlay": re.sub(r'/', ':', str(images[3])), "width": 440, "height": 280, "y": 140, "x": 220, "crop": "fill"}])
    return Response({"image": url})



