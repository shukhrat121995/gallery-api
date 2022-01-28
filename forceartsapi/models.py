from django.db import models
from django.core.validators import FileExtensionValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator


class TitleField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(TitleField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title = TitleField(max_length=255, null=True, blank=False, unique=True)

    description = models.TextField(null=True, blank=False)

    image = models.ImageField(upload_to='characters', null=True)

    rank = models.IntegerField(
        unique=True,
        null=True,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.title


def make_file_path(instance, filename):
    file_path = instance.collection.title
    return f'images/{file_path}/{filename}'


class Wallpaper(models.Model):
    class Meta:
        verbose_name = "Wallpaper"
        verbose_name_plural = "Wallpapers"

    collection = models.ForeignKey(Category, on_delete=models.CASCADE)

    description = models.TextField(default=None, null=True)

    visibility = models.BooleanField(default=True, blank=True)

    image = models.ImageField(
        upload_to=make_file_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])],
        null=True,
    )

    tags = TaggableManager()

    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(250, 200)],
                                     format='JPEG',
                                     options={'quality': 85})

    upload_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    views = models.IntegerField(editable=False, default=0, blank=True)

    likes = models.IntegerField(editable=False, default=0, blank=True)

    def __str__(self):
        return self.collection.title


class ContactUs(models.Model):
    class Meta:
        verbose_name = "Contact-Us"
        verbose_name_plural = "Contact-Us"

    full_name = models.CharField(max_length=255, default=None, blank=True)
    email = models.EmailField(default=None, blank=True)
    message = models.TextField(default=None, blank=True)

    def __str__(self):
        return self.full_name
