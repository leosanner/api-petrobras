from __future__ import annotations

import factory
from django.contrib.auth import get_user_model

from apps.accounts.models import EmailVerification, PasswordResetCode

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.django.Password("testpass123")
    is_active = True


class EmailVerificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailVerification

    user = factory.SubFactory(UserFactory)


class PasswordResetCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PasswordResetCode

    user = factory.SubFactory(UserFactory)
