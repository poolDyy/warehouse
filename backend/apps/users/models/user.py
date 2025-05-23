from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel


class UserManager(BaseUserManager):
    """Менеджер для управления Участниками (User)."""

    def create_user(
        self,
        email: str,
        password: str,
    ) -> 'User':
        if not email:
            raise ValueError(_('The Email field must be set'))
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
    ) -> 'User':
        user = self.create_user(
            email,
            password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(
    AbstractBaseUser,
    PermissionsMixin,
    TimeStampedModel,
):
    """Модель пользователя приложения."""

    email = models.EmailField(
        verbose_name=_('Электронная почта'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _('Пользователь с такой почтой уже существует'),
        },
    )

    is_active = models.BooleanField(
        verbose_name=_('Активный'),
        default=True,
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email
