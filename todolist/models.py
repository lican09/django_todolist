# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser,\
    PermissionsMixin, BaseUserManager
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text = _('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text = _('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    qq = models.CharField(max_length=13, verbose_name='qq')
    phone = models.CharField(max_length=11, verbose_name='phone')
    reg_ip = models.CharField(max_length=15, verbose_name='reg_ip', blank=True, unique=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name


class Item(models.Model):
    user = models.ForeignKey(UserProfile)
    content = models.CharField(max_length=200, verbose_name=u"事项内容")
    is_done = models.BooleanField(default=False, verbose_name=u"事项状态")
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name=u"发布时间")

    class Meta:
        verbose_name = "待办事项"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.content

