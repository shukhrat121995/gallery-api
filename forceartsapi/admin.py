from django.contrib import admin
from .models import Category, Wallpaper, ContactUs
from imagekit.admin import AdminThumbnail


class WallpaperInline(admin.TabularInline):
    model = Wallpaper
    extra = 1

    def get_queryset(self, request):
        LIMIT_SEARCH = 3
        queryset = super(WallpaperInline, self).get_queryset(request)
        ids = queryset.order_by('-id').values('pk')[:LIMIT_SEARCH]
        qs = Wallpaper.objects.filter(pk__in=ids).order_by('-id')
        return qs


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'image', 'rank']
    search_fields = ['title']
    inlines = [WallpaperInline]
    list_per_page = 50


@admin.register(Wallpaper)
class WallpaperAdmin(admin.ModelAdmin):
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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    image_thumbnail = AdminThumbnail(image_field='image_thumbnail')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'message']
    list_per_page = 50
