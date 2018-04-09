from rest_framework import serializers
from images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_id', 'inplace_tags', 'image')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tags = instance.inplace_tags.split(';')
        ret['inplace_tags'] = tags
        ret['image'] = instance.image.build_url()
        return ret

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        if isinstance(data['inplace_tags'], list):
            data['inplace_tags'] = ';'.join(data['inplace_tags'])
        validated_data['inplace_tags'] = data['inplace_tags']
        return validated_data
