from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.urls import reverse

from django.db.models.signals import post_save

from .utils import code_generator

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


#email
from django.core.mail import send_mail


class NorthUserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class NorthUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = NorthUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        # The user is identified by their email address
        return str(self.email)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):

    user            = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name      = models.CharField(max_length=50,null=True, blank=True)
    last_name       = models.CharField(max_length=50,null=True, blank=True)
    city            = models.CharField(max_length=25,null=True, blank=True)
    country         = models.CharField(max_length=25,null=True, blank=True)


    def __str__(self):
        return str(self.user.email)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print('sda')
        try:
            Profile.objects.create(user=instance)
            ActivationProfile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)



class ActivationProfile(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL)
    key     = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = code_generator()
        super(ActivationProfile, self).save(*args, **kwargs)


def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
    if created:
            print('email')
            message = "http://127.0.0.1:9090/accounts/activate/" + instance.key
            mail_to = 'shashank.ragireddy@gmail.com'
            #print(mail_to)
            send_mail('North user activation',message,'django.10dnorth@gmail.com',[mail_to])
            #url = http://127.0.0.0:9090/activate/ + instance.key
            #print('email3')
            #print('activation created')

post_save.connect(post_save_activation_receiver, sender=ActivationProfile)
