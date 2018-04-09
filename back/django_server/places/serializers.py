from rest_framework import serializers

from places.models import ProtoPlace, ImageAttach
import ast


class SimpleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAttach
        fields = ('image',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = instance.image.build_url()
        return ret


class InfoPlaceSerializer(serializers.ModelSerializer):
    location = serializers.DictField(default={}, child=serializers.FloatField())
    images = SimpleImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProtoPlace
        fields = ('event_id', 'description', 'title', 'address', 'timetable', 'location', 'images')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['location'] = {"longitude": instance.longitude, "latitude": instance.latitude}
        return ret

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        if isinstance(data['location'], str):
            location = ast.literal_eval(data['location'])
        else:
            location = data['location']
        validated_data['latitude'] = location['latitude']
        validated_data['longitude'] = location['longitude']
        return validated_data

    def create(self, validated_data):
        r = dict(validated_data)
        del r['location']
        return ProtoPlace.objects.create(**r)


class SimplePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtoPlace
        fields = ('event_id', 'inplace_tags')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tags = instance.inplace_tags.split(';')
        ret['inplace_tags'] = tags
        return ret

    def to_internal_value(self, data):
        validated_data = dict()
        validated_data['event_id'] = data['event_id']
        if isinstance(data['inplace_tags'], list):
            data['inplace_tags'] = ';'.join(data['inplace_tags'])
        validated_data['inplace_tags'] = data['inplace_tags']
        return validated_data


class ProtoPlaceSerializer(serializers.ModelSerializer):
    location = serializers.DictField(default={}, child=serializers.FloatField())
    images = SimpleImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProtoPlace
        fields = ('event_id', 'description', 'title', 'address', 'timetable', 'location', 'inplace_tags', 'images')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['location'] = {"longitude": instance.longitude, "latitude": instance.latitude}
        tags = instance.inplace_tags.split(';')
        ret['inplace_tags'] = tags
        return ret

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        if isinstance(data['location'], str):
            location = ast.literal_eval(data['location'])
        else:
            location = data['location']
        validated_data['latitude'] = location['latitude']
        validated_data['longitude'] = location['longitude']
        if isinstance(data['inplace_tags'], list):
            data['inplace_tags'] = ';'.join(data['inplace_tags'])
        validated_data['inplace_tags'] = data['inplace_tags']
        return validated_data

    def create(self, validated_data):
        r = dict(validated_data)
        del r['location']
        return ProtoPlace.objects.create(**r)


class ImageSerializer(serializers.ModelSerializer):
    place = serializers.SlugRelatedField(slug_field='event_id', queryset=ProtoPlace.objects.all())

    class Meta:
        model = ImageAttach
        fields = ('id', 'image', 'place')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = instance.image.build_url()
        return ret

