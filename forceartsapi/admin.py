"""Admin panel configuration file

Contains category, wallpaper and contact
"""
from django.contrib import admin
from imagekit.admin import AdminThumbnail
from .models import Category, Wallpaper, ContactUs


class WallpaperInline(admin.TabularInline):
    """Helper class for WallpaperAdmin"""

    model = Wallpaper
    extra = 1

    def get_queryset(self, request) -> object:
        """Returns the latest three wallpapers
        Args:
            request:
        Returns:
            object:
        """
        # pylint: disable=no-member
        queryset = super().get_queryset(request)
        ids = queryset.order_by('-id').values('pk')[:3]
        return Wallpaper.objects.filter(pk__in=ids).order_by('-id')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Displays list of categories"""

    list_display = ['title', 'description', 'image', 'rank']
    search_fields = ['title']
    inlines = [WallpaperInline]
    list_per_page = 50


@admin.register(Wallpaper)
class WallpaperAdmin(admin.ModelAdmin):
    """Displays list of wallpapers"""

    list_display = [
        'id',
        'collection',
        'description',
        'tag_list',
        'visibility',
        'image_thumbnail',
        'upload_time',
        'views',
        'likes'
    ]
    search_fields = [
        'collection__title',
        'description',
        'tags__name'
    ]
    autocomplete_fields = ['collection']
    list_per_page = 50

    def get_queryset(self, request: object) -> object:
        """
        Args:
            request:
        Returns:
            object:
        """
        return super().get_queryset(request).prefetch_related('tags')

    @classmethod
    def tag_list(cls, obj: object) -> object:
        """
        Args:
            obj:
        Returns:
            object:
        """
        return ", ".join(o.name for o in obj.tags.all())

    image_thumbnail = AdminThumbnail(image_field='image_thumbnail')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    """Displays list of contacts"""

    list_display = ['full_name', 'email', 'message']
    list_per_page = 50
