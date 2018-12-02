from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

#settings
from django.conf import settings

#validators
from django.core.validators import RegexValidator

#utils
# from .utils import code_generator

#email
from django.core.mail import send_mail


#signals
from django.db.models.signals import post_save

from django.core.urlresolvers import reverse
# Create your models here.

Users = settings.AUTH_USER_MODEL


from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


USERNAME_REGEX = '^[a-zA-X][a-zA-X0-9]{6,10}*$'
FNAME_REGEX = '^[a-zA-X][a-zA-Z]{6,10}*$'
LNAME_REGEX = '^[a-zA-X][a-zA-X]{6,10}*$'

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=125,
                                validators=[RegexValidator(regex=FNAME_REGEX,
                                            message='first name must be alphabetic',
                                            code='Invalid first name')
                                            ],
                                )

    last_name = models.CharField(max_length=125,
                                validators=[RegexValidator(regex=LNAME_REGEX,
                                            message='last name must be alphabetic',
                                            code='Invalid last name')
                                            ],

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

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


    objects = UserManager()


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name = self.first_name,
            last_name = self.last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            print('user created')
            Profile.objects.create(user=instance)
            ActivationProfile.objects.create(user=instance)
            print('done')
        except:
            pass

post_save.connect(post_save_user_model_receiver,sender=settings.AUTH_USER_MODEL)



class Profile(models.Model):

    user     = models.OneToOneField(settings.AUTH_USER_MODEL)
    city     = models.CharField(max_length=25,null=True, blank=True)
    country  = models.CharField(max_length=25,null=True, blank=True)


    def __str__(self):
        return str(self.user.username)



class ActivationProfile(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL)
    key     = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = code_generator()
        super(ActivationProfile, self).save(*args, **kwargs)


def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
    if created:
        #print('email')
        message = "http://127.0.0.1:9090/accounts/activate/" + instance.key
        send_mail('vogue user activation',message,'django.10dnorth@gmail.com',['shashank.ragireddy@gmail.com'])
        #url = http://127.0.0.0:9090/activate/ + instance.key
        #print('email3')
        #print('activation created')

post_save.connect(post_save_activation_receiver, sender=ActivationProfile)
