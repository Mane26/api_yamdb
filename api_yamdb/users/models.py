from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from api_yamdb.settings import message_for_reservad_name, reserved_name


USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"
ROLES = [
    ("user", USER),
    ("moderator", MODERATOR),
    ("admin", ADMIN)
]


class MyUserManager(UserManager):
    """Сохраняет пользователя только с email.
    Зарезервированное имя использовать нельзя."""
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательное')
        if username == reserved_name:
            raise ValueError(message_for_reservad_name)
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)


class User(AbstractUser):
    """Класс пользователей."""
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=max(len(role) for _, role in ROLES),
        choices=ROLES,
        default=USER
    )
    username = models.CharField(max_length=150, unique=True, db_index=True)
    objects = MyUserManager()
    email = models.EmailField(
        max_length=254, verbose_name='email',
        unique=True)

    REQUIRED_FIELDS = ('email', 'password')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
