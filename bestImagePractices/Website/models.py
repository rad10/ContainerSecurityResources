import os
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    #email = models.EmailField(_('email address'), unique=True)
    email = models.EmailField(max_length=75, db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# File upload models

class Upload(models.Model):
    title = models.CharField(max_length=120)
    number = models.TextField(blank=True)
    date = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=1)


class FileUpload(models.Model):
    def file_size(value):
        limit = 20 * 1024 * 1024
        if value.size > limit:
            raise ValidationError("File size too large... (>20MB)")

    title = models.CharField(max_length=64)
    upload_time = models.DateTimeField(auto_now_add=True, blank=True)
    file = models.FileField(upload_to="", validators=[
                            file_size, FileExtensionValidator(allowed_extensions=['gcode'])])
    upload_by = models.EmailField(
        max_length=75, unique=False, default='test@my.fit.com')


# When Django receives signal to delete a FileUpload object, this will be called and delete the file from the filesystem
@receiver(models.signals.post_delete, sender=FileUpload)
def remove_file(sender, instance, **kwargs):
    if instance.file:
        # TODO: Once we take over from previous group, send out the file to the 3D printer for printing
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
