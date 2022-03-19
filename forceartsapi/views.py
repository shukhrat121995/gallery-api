"""Application views module"""
from django.http import JsonResponse, Http404
from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .generic import get_or_none
from .models import Wallpaper, Category, ContactUs
from .serializers import WallpaperSerializer, CategorySerializer, ContactUsSerializer


def infinite_search(request):
    """
    Args:
        request:
    Returns:
        object:
    """
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    query = request.GET.get('query')
    order = request.GET.get('order', 'upload_time')

    if query:
        return Wallpaper.objects.filter(
            Q(visibility=True) &
            (
                    Q(tags__name__in=[str(query)]) |
                    Q(collection__title=str(query).lower())
            )
        ).distinct().order_by(f'-{str(order)}')[int(offset):int(offset) + int(limit)]
    return Wallpaper.objects.filter(
        visibility=True
    ).order_by(f'-{str(order)}')[int(offset):int(offset) + int(limit)]


def is_there_more_data_search(request):
    """
    Args:
        request:
    Returns:
        value: True or False
    """
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    query = request.GET.get('query')

    if query:
        return int(offset) + int(limit) < Wallpaper.objects.filter(
            Q(visibility=True) &
            (
                    Q(tags__name__in=[str(query)]) |
                    Q(collection__title=str(query).lower())
            )
        ).distinct().count()
    return int(offset) + int(limit) < Wallpaper.objects.filter(visibility=True).count()


class CategoryView(generics.ListAPIView):
    """Category API view"""
    queryset = Category.objects.all().order_by('rank')
    serializer_class = CategorySerializer


class ReactInfiniteSearchView(generics.ListAPIView):
    """Generic infinite scrolling view"""
    serializer_class = WallpaperSerializer

    def get_queryset(self):
        """
        Returns:
            object:
        """
        return infinite_search(self.request)

    def list(self, request, *args, **kwargs):
        """
        Args:
            request:
            *args:
            **kwargs:
        Returns:
            response: JSON
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(
            queryset, many=True, context={
                "request": request})
        return Response({
            "images": serializer.data,
            "has_more": is_there_more_data_search(request)
        })


class ContactUsView(generics.ListCreateAPIView):
    """ContactUS generic API view"""
    permission_classes = (AllowAny,)
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


class WallpaperApiView(APIView):
    """Increase and decrease wallpaper's like value"""
    permission_classes = (AllowAny,)
    serializer_class = WallpaperSerializer

    def patch(self, request, primary_key):
        """Increments or decrements wallpaper's likes value"""
        wallpaper_object = get_or_none(Wallpaper, pk=primary_key)
        options = ('inc-likes', 'dec-likes', 'inc-views')
        option = request.data.get('option', None)

        if not option or option not in options:
            return JsonResponse(
                status=422,
                data={
                    'status': 'false',
                    'message': 'option value incorrect'
                }
            )
        if not wallpaper_object:
            return JsonResponse(
                status=404,
                data={
                    'status': 'false',
                    'message': 'wallpaper with given id not found'
                }
            )
        if option == 'inc-likes':
            wallpaper_object.likes += 1
        elif option == 'dec-likes':
            wallpaper_object.likes -= 1
        else:
            wallpaper_object.views += 1

        wallpaper_object.save()
        serializer = WallpaperSerializer(wallpaper_object)
        return Response(serializer.data)
