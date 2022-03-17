from .models import Wallpaper, Category, ContactUs
from rest_framework import serializers


class WallpaperSerializer(serializers.ModelSerializer):

    collection = serializers.SlugRelatedField(
        read_only=True, slug_field='title')
    image = serializers.ImageField(
        max_length=None,
        use_url=True,
        allow_null=True,
        required=False)
    image_thumbnail = serializers.ImageField()
    upload_time = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = Wallpaper
        fields = [
            'id',
            'collection',
            'description',
            'image',
            'image_thumbnail',
            'upload_time',
            'views',
            'likes']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'image', 'rank']


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'full_name', 'email', 'message']
