"""This module contains serializer class for Wallpaper, Category and Contact"""
from rest_framework import serializers
from .models import Wallpaper, Category, ContactUs


class RelatedCategorySerializer(serializers.ModelSerializer):
    """Serializer for custom Hyperlink representation"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Category serializer representation"""
        model = Category
        fields = ['id', 'title', 'url']
    # pylint: enable=too-few-public-methods


class CreateAndUpdateWallpaperSerializer(serializers.ModelSerializer):
    """Only for creating and updating wallpaper"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Wallpaper serializer representation"""
        model = Wallpaper
        fields = '__all__'
    # pylint: enable=too-few-public-methods


class WallpaperSerializer(serializers.ModelSerializer):
    """This class contains wallpaper serializer"""

    collection = RelatedCategorySerializer(required=False)
    image = serializers.ImageField(
        max_length=None,
        use_url=True,
        allow_null=True,
        required=False
    )
    image_thumbnail = serializers.ImageField(
        max_length=None,
        use_url=True,
        allow_null=True,
        required=False
    )

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
            'likes'
        ]
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
