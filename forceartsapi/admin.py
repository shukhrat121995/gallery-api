"""Admin panel configuration file
Contains category, wallpaper and contact
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from imagekit.admin import AdminThumbnail
from .models import Category, Wallpaper, ContactUs, User


class UserAdmin(BaseUserAdmin):
    """Custom user admin page"""
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


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


admin.site.register(User, UserAdmin)
