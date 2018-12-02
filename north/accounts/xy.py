from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

#settings
from django.conf import settings

#validators
from django.core.validators import RegexValidator

#utils
from .utils import code_generator

#email
from django.core.mail import send_mail


#signals
from django.db.models.signals import post_save

from django.core.urlresolvers import reverse
# Create your models here.

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


#USERNAME_REGEX = '^[a-zA-X][a-zA-X0-9]{6,10}*$'
FNAME_REGEX = '^[a-zA-X][a-zA-Z]*$'
LNAME_REGEX = '^[a-zA-X][a-zA-X]*$'



class NorthUserManager(BaseUserManager):
    def create_user(self, username, password=None,is_staff=False,is_admin=False,active=True):
        """
        Creates and saves a User with the given email and password.
        """

        if not username:
            raise ValueError('Users must have an username address')

        user = self.model(
            username=self.normalize_email(username)
        )

        user.set_password(password)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.active   = active
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, first_name, last_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            password=password,
            is_staff=True,
            is_admin=True,
            )
        return user


class NorthUser(AbstractBaseUser):
    username = models.EmailField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )


    active = models.BooleanField(default=True) #can login (in general)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.


    objects = NorthUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] # USERNAME_FIELD & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active






# def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#
#         try:
#             #print('user created')
#             Profile.objects.create(user=instance)
#             ActivationProfile.objects.create(user=instance)
#             #print('done')
#         except:
#             pass
#
# post_save.connect(post_save_user_model_receiver,sender=NorthUser)
#
#
#
# class Profile(models.Model):
#
#     user     = models.OneToOneField(NorthUser)
#     first_name = models.CharField(max_length=125,
#                                 validators=[RegexValidator(regex=FNAME_REGEX,
#                                             message='first name must be alphabetic',
#                                             code='Invalid first name')
#                                             ],blank=True,null=True)
#
#     last_name = models.CharField(max_length=125,
#                                 validators=[RegexValidator(regex=LNAME_REGEX,
#                                             message='last name must be alphabetic',
#                                             code='Invalid last name')
#                                             ],blank=True,null=True)
#
#     city     = models.CharField(max_length=25,null=True, blank=True)
#     country  = models.CharField(max_length=25,null=True, blank=True)
#
#
#     def __str__(self):
#         return str(self.user.username)


#
# class ActivationProfile(models.Model):
#     user    = models.ForeignKey(NorthUser)
#     key     = models.CharField(max_length=120)
#     expired = models.BooleanField(default=False)
#
#     def save(self, *args, **kwargs):
#         self.key = code_generator()
#         super(ActivationProfile, self).save(*args, **kwargs)
#
#
# def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         #print('email')
#         message = "http://127.0.0.1:9090/accounts/activate/" + instance.key
#         mail_to = 'shashank.ragireddy@gmail.com'
#         #print(mail_to)
#         send_mail('North user activation',message,'django.10dnorth@gmail.com',[mail_to])
#         #url = http://127.0.0.0:9090/activate/ + instance.key
#         #print('email3')
#         #print('activation created')
#
# post_save.connect(post_save_activation_receiver, sender=ActivationProfile)
