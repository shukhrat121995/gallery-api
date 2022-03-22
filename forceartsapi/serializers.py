"""This module contains serializer class for Wallpaper, Category and Contact"""
from rest_framework import serializers
from .models import Wallpaper, Category, ContactUs


class WallpaperSerializer(serializers.ModelSerializer):
    """This class does wallpaper serializer"""
    collection = serializers.SlugRelatedField(
        read_only=True, slug_field='title')
    image = serializers.ImageField(
        max_length=None,
        use_url=True,
        allow_null=True,
        required=False)
    image_thumbnail = serializers.ImageField()
    upload_time = serializers.DateTimeField(format="%d-%m-%Y")

    # pylint: disable=too-few-public-methods
    class Meta:
        """Wallpaper class representation"""
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
    # pylint: enable=too-few-public-methods


class CategorySerializer(serializers.ModelSerializer):
    """This class contains category serializer"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Category class representation"""
        model = Category
        fields = ['id', 'title', 'description', 'image', 'rank']
    # pylint: enable=too-few-public-methods


class ContactUsSerializer(serializers.ModelSerializer):
    """This class contains contact serializer"""
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    message = serializers.CharField()

    # pylint: disable=too-few-public-methods
    class Meta:
        """Contact class representation"""
        model = ContactUs
        fields = ['id', 'full_name', 'email', 'message']
    # pylint: enable=too-few-public-methods
