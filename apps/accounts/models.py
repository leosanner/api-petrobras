from __future__ import annotations

import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Manager that uses email as the unique identifier."""

    use_in_migrations = True

    def _create_user(
        self,
        email: str,
        username: str,
        password: str | None,
        **extra_fields,
    ) -> User:
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        username: str,
        password: str | None = None,
        **extra_fields,
    ) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        username: str,
        password: str | None = None,
        **extra_fields,
    ) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    """Custom user model using email as the login identifier."""

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email


def _generate_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


class BaseVerificationCode(models.Model):
    """Abstract base for single-use verification codes with expiration.

    Subclasses must define their own ``EXPIRATION_MINUTES`` and a concrete
    ``user`` ForeignKey (so each subclass gets its own ``related_name``).
    """

    EXPIRATION_MINUTES: int = 15

    code = models.CharField(max_length=6, default=_generate_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def save(self, *args, **kwargs) -> None:
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(
                minutes=self.EXPIRATION_MINUTES
            )
        super().save(*args, **kwargs)

    def is_valid(self) -> bool:
        return self.used_at is None and timezone.now() < self.expires_at

    def mark_used(self) -> None:
        self.used_at = timezone.now()
        self.save(update_fields=["used_at"])


class EmailVerification(BaseVerificationCode):
    """Single-use email verification code (15 min expiration)."""

    EXPIRATION_MINUTES = 15

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verifications",
    )

    def __str__(self) -> str:
        return f"EmailVerification(user={self.user_id}, code={self.code})"


class PasswordResetCode(BaseVerificationCode):
    """Single-use password reset code (30 min expiration)."""

    EXPIRATION_MINUTES = 30

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_codes",
    )

    def __str__(self) -> str:
        return f"PasswordResetCode(user={self.user_id}, code={self.code})"
