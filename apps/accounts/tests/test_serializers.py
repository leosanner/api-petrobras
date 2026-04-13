from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

from apps.accounts.factories import EmailVerificationFactory, UserFactory
from apps.accounts.serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
    VerifyEmailSerializer,
)

User = get_user_model()


@pytest.mark.django_db
class TestRegisterSerializer:
    def test_valid_data(self):
        data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "strong!Pass1",
            "password_confirm": "strong!Pass1",
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_password_mismatch(self):
        data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "strong!Pass1",
            "password_confirm": "differentPass1",
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "password_confirm" in serializer.errors

    def test_weak_password(self):
        data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "123",
            "password_confirm": "123",
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_duplicate_email(self):
        UserFactory(email="taken@example.com")
        data = {
            "email": "taken@example.com",
            "username": "another",
            "password": "strong!Pass1",
            "password_confirm": "strong!Pass1",
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_missing_fields(self):
        serializer = RegisterSerializer(data={})
        assert not serializer.is_valid()
        assert "email" in serializer.errors
        assert "username" in serializer.errors
        assert "password" in serializer.errors


@pytest.mark.django_db
class TestVerifyEmailSerializer:
    def test_valid_code(self):
        user = UserFactory(is_active=False)
        verification = EmailVerificationFactory(user=user)
        data = {"email": user.email, "code": verification.code}
        serializer = VerifyEmailSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_invalid_code(self):
        user = UserFactory(is_active=False)
        EmailVerificationFactory(user=user)
        data = {"email": user.email, "code": "000000"}
        serializer = VerifyEmailSerializer(data=data)
        assert not serializer.is_valid()

    def test_nonexistent_email(self):
        data = {"email": "nobody@example.com", "code": "123456"}
        serializer = VerifyEmailSerializer(data=data)
        assert not serializer.is_valid()


@pytest.mark.django_db
class TestLoginSerializer:
    def test_valid_credentials(self):
        UserFactory(email="login@example.com")
        data = {"email": "login@example.com", "password": "testpass123"}
        serializer = LoginSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_missing_fields(self):
        serializer = LoginSerializer(data={})
        assert not serializer.is_valid()
        assert "email" in serializer.errors
        assert "password" in serializer.errors


class TestPasswordResetRequestSerializer:
    def test_valid_email(self):
        data = {"email": "any@example.com"}
        serializer = PasswordResetRequestSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_missing_email(self):
        serializer = PasswordResetRequestSerializer(data={})
        assert not serializer.is_valid()
        assert "email" in serializer.errors


@pytest.mark.django_db
class TestPasswordResetConfirmSerializer:
    def test_valid_data(self):
        data = {
            "email": "user@example.com",
            "code": "123456",
            "new_password": "newStrong!1",
            "new_password_confirm": "newStrong!1",
        }
        serializer = PasswordResetConfirmSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_password_mismatch(self):
        data = {
            "email": "user@example.com",
            "code": "123456",
            "new_password": "newStrong!1",
            "new_password_confirm": "different!1",
        }
        serializer = PasswordResetConfirmSerializer(data=data)
        assert not serializer.is_valid()
        assert "new_password_confirm" in serializer.errors

    def test_weak_password(self):
        data = {
            "email": "user@example.com",
            "code": "123456",
            "new_password": "123",
            "new_password_confirm": "123",
        }
        serializer = PasswordResetConfirmSerializer(data=data)
        assert not serializer.is_valid()
        assert "new_password" in serializer.errors


@pytest.mark.django_db
class TestPasswordChangeSerializer:
    def test_valid_data(self):
        data = {
            "current_password": "old_pass",
            "new_password": "newStrong!1",
            "new_password_confirm": "newStrong!1",
        }
        serializer = PasswordChangeSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_password_mismatch(self):
        data = {
            "current_password": "old_pass",
            "new_password": "newStrong!1",
            "new_password_confirm": "different!1",
        }
        serializer = PasswordChangeSerializer(data=data)
        assert not serializer.is_valid()
        assert "new_password_confirm" in serializer.errors


@pytest.mark.django_db
class TestUserSerializer:
    def test_serializes_user(self):
        user = UserFactory()
        data = UserSerializer(user).data
        assert data["id"] == user.id
        assert data["email"] == user.email
        assert data["username"] == user.username
        assert "password" not in data
