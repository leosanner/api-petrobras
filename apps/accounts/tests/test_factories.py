from __future__ import annotations

import pytest

from apps.accounts.factories import (
    EmailVerificationFactory,
    PasswordResetCodeFactory,
    UserFactory,
)
from apps.accounts.models import EmailVerification, PasswordResetCode, User


@pytest.mark.django_db
class TestUserFactory:
    def test_creates_user(self):
        user = UserFactory()
        assert isinstance(user, User)
        assert user.pk is not None
        assert user.email
        assert user.username

    def test_creates_user_with_hashed_password(self):
        user = UserFactory()
        assert user.check_password("testpass123")

    def test_creates_inactive_user(self):
        user = UserFactory(is_active=False)
        assert user.is_active is False


@pytest.mark.django_db
class TestEmailVerificationFactory:
    def test_creates_verification(self):
        verification = EmailVerificationFactory()
        assert isinstance(verification, EmailVerification)
        assert verification.pk is not None
        assert len(verification.code) == 6
        assert verification.user is not None

    def test_creates_verification_for_given_user(self):
        user = UserFactory()
        verification = EmailVerificationFactory(user=user)
        assert verification.user == user


@pytest.mark.django_db
class TestPasswordResetCodeFactory:
    def test_creates_reset_code(self):
        code = PasswordResetCodeFactory()
        assert isinstance(code, PasswordResetCode)
        assert code.pk is not None
        assert len(code.code) == 6
        assert code.user is not None

    def test_creates_reset_code_for_given_user(self):
        user = UserFactory()
        code = PasswordResetCodeFactory(user=user)
        assert code.user == user
