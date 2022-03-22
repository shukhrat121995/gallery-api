"""
This module contains models for Category, Wallpaper and ContactUs tables class representation
There are several helper methods and classes such asa TitleField and make_file_path()
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator, MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager


class UserManager(BaseUserManager):
    """Helper class for a User class"""
    def create_user(self, email, password=None, **kwargs):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class TitleField(models.CharField):
    """This class helps to convert Wallpaper's title to lowercase"""

    # pylint: disable=W0235
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """
        Args:
            value: title with capital letters
        Returns:
            object: title in lowercase
        """
        return str(value).lower()


class Category(models.Model):
    """Category class representation"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Sets plural and singular model name"""
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    # pylint: enable=too-few-public-methods

    title = TitleField(max_length=255, null=True, blank=False, unique=True)
    description = models.TextField(null=True, blank=False)
    image = models.ImageField(upload_to='characters', null=True)
    rank = models.IntegerField(
        unique=True,
        null=True,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        """
        Returns: string representation of a model
        """
        return str(self.title)


def make_file_path(instance, filename):
    """
    Args:
        instance:
        filename:
    Returns:
        value: file path
    """
    file_path = instance.collection.title
    return f'images/{file_path}/{filename}'


class Wallpaper(models.Model):
    """Wallpaper class representation"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Sets plural and singular model name"""
        verbose_name = "Wallpaper"
        verbose_name_plural = "Wallpapers"
    # pylint: enable=too-few-public-methods

    collection = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(default=None, null=True)
    visibility = models.BooleanField(default=True, blank=True)
    image = models.ImageField(
        upload_to=make_file_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'jpeg',
                    'png',
                    'jpg'
                ]
            )
        ],
        null=True,
    )
    tags = TaggableManager()
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(250, 200)],
        format='JPEG',
        options={'quality': 85}
    )
    upload_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    views = models.IntegerField(editable=False, default=0, blank=True)
    likes = models.IntegerField(editable=False, default=0, blank=True)

    def __str__(self):
        """
        Returns: string representation of a model
        """
        # pylint: disable=E1101
        return str(self.collection.title)


class ContactUs(models.Model):
    """ContactUs class representation"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Sets plural and singular model name"""
        verbose_name = "Contact-Us"
        verbose_name_plural = "Contact-Us"
    # pylint: enable=too-few-public-methods

    full_name = models.CharField(max_length=255, default=None, blank=True)
    email = models.EmailField(default=None, blank=True)
    message = models.TextField(default=None, blank=True)

    def __str__(self):
        """
        Returns: string representation of a model
        """
        return str(self.full_name)
