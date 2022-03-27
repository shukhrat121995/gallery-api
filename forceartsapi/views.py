"""Application views module"""
from django.http import JsonResponse, Http404
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status, viewsets, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Wallpaper, Category
from .serializers import WallpaperSerializer, \
    CreateAndUpdateWallpaperSerializer, CategorySerializer, ContactUsSerializer
from .permissions import CreateAndUpdate

CACHED_TIME_DURATION = 60 * 60 * 2


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


class CategoryViewSet(viewsets.ViewSet):
    """Category API ViewSet class"""
    serializer_class = CategorySerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated | CreateAndUpdate]

    def get_object(self, pk):
        """Returns wallpaper object or raise an error"""
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist as category_not_exist:
            raise Http404 from category_not_exist

    def list(self, request):
        """Retrieves all categories"""
        categories = Category.objects.all().order_by('rank')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(CACHED_TIME_DURATION))
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        """Creates a new wallpaper"""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle updating an object"""
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Hande removing an object"""
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class ContactUsView(APIView):
    """ContactUS generic API view"""
    serializer_class = ContactUsSerializer

    def post(self, request):
        """Creates a new contact entity"""
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WallpaperViewSet(viewsets.ViewSet):
    """Wallpaper API ViewSet class"""
    serializer_class = WallpaperSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated | CreateAndUpdate]

    def get_object(self, pk):
        """Returns wallpaper object or raise an error"""
        try:
            return Wallpaper.objects.get(pk=pk)
        except Wallpaper.DoesNotExist as wallpaper_not_exist:
            raise Http404 from wallpaper_not_exist

    @method_decorator(cache_page(CACHED_TIME_DURATION))
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        wallpaper = self.get_object(pk)
        serializer = WallpaperSerializer(wallpaper, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Creates a new wallpaper"""
        serializer = CreateAndUpdateWallpaperSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle updating an object"""
        wallpaper = self.get_object(pk)
        serializer = CreateAndUpdateWallpaperSerializer(wallpaper, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        wallpaper = self.get_object(pk)
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
        if option == 'inc-likes':
            wallpaper.likes += 1
        elif option == 'dec-likes':
            wallpaper.likes -= 1
        else:
            wallpaper.views += 1

        wallpaper.save()
        serializer = WallpaperSerializer(wallpaper, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Hande removing an object"""
        wallpaper = self.get_object(pk)
        wallpaper.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
