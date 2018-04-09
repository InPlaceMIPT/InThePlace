from django.contrib import admin
from django.db import models
from cloudinary import models as clm


class ProtoPlace(models.Model):
    event_id = models.IntegerField(unique=True)
    inplace_tags = models.TextField(default='notag')
    title = models.CharField(default='default_title', max_length=255)
    address = models.CharField(default='def_address', max_length=255)
    timetable = models.CharField(default='24/7', max_length=255)
    description = models.TextField(default='def_description')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return 'event %d' % self.event_id


class ImageAttach(models.Model):
    image = clm.CloudinaryField('image')
    place = models.ForeignKey(ProtoPlace, to_field='event_id', on_delete=models.CASCADE, related_name='images')


class CategoryKudaGo(models.Model):
    name = models.CharField(max_length=255)


class PlaceKudaGo(models.Model):
    event_id = models.IntegerField()
    kudago_id = models.IntegerField(default=-1)
    title = models.CharField(default='default_title', max_length=255)
    slug = models.SlugField(default='def_slug', max_length=255)
    address = models.CharField(default='def_address', max_length=255)
    timetable = models.CharField(default='24/7', max_length=255)
    phone = models.CharField(default='def_phone', max_length=20)
    is_stub = models.BooleanField(default=False)
    body_text = models.TextField(default='def_text')
    description = models.TextField(default='def_description')
    site_url = models.URLField(default='def_site', max_length=255)
    foreign_url = models.URLField(default='def_fsite', max_length=255)
    coords_lat = models.FloatField(default=0.0)
    coords_lon = models.FloatField(default=0.0)
    subway = models.CharField(default='def_subway', max_length=255)
    favorites_count = models.IntegerField(default=-1)
    comments_count = models.IntegerField(default=-1)
    is_closed = models.BooleanField(default=False)
    categories = models.ManyToManyField(CategoryKudaGo, related_name='places')
    short_title = models.CharField(max_length=255, default='def_stitle')
    tags = models.TextField(default='notag;')
    location = models.CharField(max_length=255, default='msk')
    age_restriction = models.CharField(max_length=20, default='0')
    disable_comments = models.BooleanField(default=False)
    has_parking_lot = models.BooleanField(default=False)


class ImageKudaGo(models.Model):
    image = models.URLField(max_length=255)
    source_link = models.URLField(max_length=255)
    source_name = models.CharField(max_length=255)
    place = models.ForeignKey(PlaceKudaGo, on_delete=models.CASCADE,related_name='images')


admin.site.register(ProtoPlace)
admin.site.register(ImageAttach)

