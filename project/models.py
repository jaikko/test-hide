from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

# Create your models here.


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


class Staff(AbstractUser):

    choice = (
        ('Sale', 'Sale'),
        ('Support', 'Support'),
        ('Admin', 'Admin'),
        ('Management', 'Management')
    )

    username = None
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    team = models.CharField(max_length=20, blank=False, choices=choice, default='Admin')
    date_created = models.DateTimeField(default=now, editable=False)
    date_updated = models.DateTimeField(default=now, editable=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def update(self, *args, **kwargs):
        kwargs.update({'date_updated': now})
        super().update(*args, **kwargs)

        return self

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Client(models.Model):

    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    company_name = models.CharField(max_length=250, blank=False)
    date_created = models.DateTimeField(default=now, editable=False)
    date_updated = models.DateTimeField(default=now, editable=False)
    sale_contact = ForeignKey(Staff, on_delete=models.CASCADE, null=True)

    def update(self, *args, **kwargs):
        kwargs.update({'date_updated': now})
        super().update(*args, **kwargs)

        return self

    def __str__(self):
        return self.email


class Status(models.Model):

    status = models.CharField(max_length=20, blank=False)


class Contract(models.Model):

    date_created = models.DateTimeField(default=now, editable=False)
    date_updated = models.DateTimeField(default=now, editable=False)
    sale_contact = ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    client = ForeignKey(Client, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateTimeField()

    def update(self, *args, **kwargs):
        kwargs.update({'date_updated': now})
        super().update(*args, **kwargs)

        return self


class Event(models.Model):

    date_created = models.DateTimeField(default=now, editable=False)
    date_updated = models.DateTimeField(default=now, editable=False)
    support_contact = ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    client = ForeignKey(Client, on_delete=models.CASCADE, null=True)
    contract = ForeignKey(Contract, on_delete=models.CASCADE, null=True)
    event_status = ForeignKey(Status, on_delete=models.CASCADE)
    attendees = models.IntegerField(null=False)
    event_date = models.DateTimeField()
    notes = TextField(blank=True)
