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


class CategorySerializer(serializers.ModelSerializer):
    """This class contains category serializer"""
    class Meta:
        """Category class representation"""
        model = Category
        fields = ['id', 'title', 'description', 'image', 'rank']


class ContactUsSerializer(serializers.ModelSerializer):
    """This class contains contact serializer"""
    class Meta:
        """Contact class representation"""
        model = ContactUs
        fields = ['id', 'full_name', 'email', 'message']
