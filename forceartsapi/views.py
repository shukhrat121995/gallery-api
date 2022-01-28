from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Wallpaper, Category, ContactUs
from .serializers import WallpaperSerializer, CategorySerializer, ContactUsSerializer
from rest_framework.response import Response


def infinite_search(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    query = request.GET.get('query')
    order = request.GET.get('order', 'upload_time')  # only can by 'views' or 'upload_time', default is by upload_time
    if query:
        return Wallpaper.objects.filter(
            Q(visibility=True) &
            (
                    Q(tags__name__in=[str(query)]) |
                    Q(collection__title=str(query).lower())
            )
        ).distinct().order_by(f'-{str(order)}')[int(offset):int(offset) + int(limit)]
    else:
        return Wallpaper.objects.filter(
            visibility=True
        ).order_by(f'-{str(order)}')[int(offset):int(offset) + int(limit)]


def is_there_more_data_search(request):
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
    else:
        return int(offset) + int(limit) < Wallpaper.objects.filter(
            visibility=True
        ).count()


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('rank')
    serializer_class = CategorySerializer


class CharactersView(generics.ListAPIView):
    queryset = Category.objects.filter(rank__lte=30).order_by('rank')
    serializer_class = CategorySerializer


class ReactInfiniteSearchView(generics.ListAPIView):
    serializer_class = WallpaperSerializer

    def get_queryset(self):
        return infinite_search(self.request)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return Response({
            "images": serializer.data,
            "has_more": is_there_more_data_search(request)
        })


class ContactUsView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


def increment_views(request, pk):
    wallpaper = Wallpaper.objects.get(id=pk)
    wallpaper.views += 1
    wallpaper.save()
    return HttpResponse('success', status=status.HTTP_200_OK)


def inc_dec_likes(request, pk, value):
    wallpaper = Wallpaper.objects.get(id=pk)
    if value == 'increase':
        wallpaper.likes += 1
    elif value == 'decrease':
        wallpaper.likes -= 1
    wallpaper.save()
    return HttpResponse('success', status=status.HTTP_200_OK)
