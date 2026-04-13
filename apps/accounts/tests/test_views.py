from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.factories import (
    EmailVerificationFactory,
    PasswordResetCodeFactory,
    UserFactory,
)

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


# ── Register ─────────────────────────────────────────────────────────


@pytest.mark.django_db
class TestRegisterView:
    URL = "/api/auth/register/"

    @patch("apps.accounts.views.send_verification_email")
    def test_register_creates_inactive_user(self, mock_send, api_client):
        data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "strong!Pass1",
            "password_confirm": "strong!Pass1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email="new@example.com")
        assert user.is_active is False
        assert user.email_verifications.count() == 1
        mock_send.assert_called_once()

    @patch("apps.accounts.views.send_verification_email")
    def test_register_duplicate_email_400(self, mock_send, api_client):
        UserFactory(email="taken@example.com")
        data = {
            "email": "taken@example.com",
            "username": "another",
            "password": "strong!Pass1",
            "password_confirm": "strong!Pass1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        mock_send.assert_not_called()

    @patch("apps.accounts.views.send_verification_email")
    def test_register_duplicate_username_400(self, mock_send, api_client):
        UserFactory(username="taken")
        data = {
            "email": "new@example.com",
            "username": "taken",
            "password": "strong!Pass1",
            "password_confirm": "strong!Pass1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        mock_send.assert_not_called()

    @patch("apps.accounts.views.send_verification_email")
    def test_register_password_mismatch_400(self, mock_send, api_client):
        data = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "strong!Pass1",
            "password_confirm": "different!1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        mock_send.assert_not_called()


# ── Verify Email ─────────────────────────────────────────────────────


@pytest.mark.django_db
class TestVerifyEmailView:
    URL = "/api/auth/verify-email/"

    def test_verify_email_activates_user(self, api_client):
        user = UserFactory(is_active=False)
        verification = EmailVerificationFactory(user=user)
        data = {"email": user.email, "code": verification.code}
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.is_active is True
        verification.refresh_from_db()
        assert verification.used_at is not None

    def test_verify_email_invalid_code_400(self, api_client):
        user = UserFactory(is_active=False)
        EmailVerificationFactory(user=user)
        data = {"email": user.email, "code": "000000"}
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verify_email_expired_code_400(self, api_client):
        user = UserFactory(is_active=False)
        verification = EmailVerificationFactory(user=user)
        verification.expires_at = timezone.now() - timedelta(seconds=1)
        verification.save(update_fields=["expires_at"])
        data = {"email": user.email, "code": verification.code}
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ── Me ───────────────────────────────────────────────────────────────


@pytest.mark.django_db
class TestMeView:
    URL = "/api/auth/me/"

    def test_me_returns_user_info(self, api_client):
        user = UserFactory()
        api_client.force_authenticate(user=user)
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
        assert response.data["username"] == user.username

    def test_me_unauthenticated_403(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN


# ── Login ────────────────────────────────────────────────────────────


@pytest.mark.django_db
class TestLoginView:
    URL = "/api/auth/login/"

    def test_login_sets_session_cookie(self, api_client):
        UserFactory(email="login@example.com")
        data = {"email": "login@example.com", "password": "testpass123"}
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_200_OK
        assert "sessionid" in response.cookies

    def test_login_inactive_user_400(self, api_client):
        UserFactory(email="inactive@example.com", is_active=False)
        data = {"email": "inactive@example.com", "password": "testpass123"}
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "not active" in response.data["detail"].lower()

    def test_login_wrong_password_400(self, api_client):
        UserFactory(email="user@example.com")
        data = {"email": "user@example.com", "password": "wrongpassword"}
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_nonexistent_email_400(self, api_client):
        data = {"email": "nobody@example.com", "password": "whatever123"}
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ── Logout ───────────────────────────────────────────────────────────


@pytest.mark.django_db
class TestLogoutView:
    URL = "/api/auth/logout/"

    def test_logout_clears_session(self, api_client):
        UserFactory(email="logout@example.com")
        # Login via session (not force_authenticate) so logout actually clears it
        api_client.post(
            "/api/auth/login/",
            {"email": "logout@example.com", "password": "testpass123"},
        )
        response = api_client.post(self.URL)
        assert response.status_code == status.HTTP_200_OK
        # After logout, /me/ should fail
        me_response = api_client.get("/api/auth/me/")
        assert me_response.status_code == status.HTTP_403_FORBIDDEN

    def test_logout_unauthenticated_403(self, api_client):
        response = api_client.post(self.URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN


# ── Password Reset ───────────────────────────────────────────────────


@pytest.mark.django_db
class TestPasswordResetView:
    URL = "/api/auth/password-reset/"

    @patch("apps.accounts.views.send_password_reset_email")
    def test_password_reset_sends_email(self, mock_send, api_client):
        user = UserFactory(email="reset@example.com")
        response = api_client.post(self.URL, {"email": "reset@example.com"})
        assert response.status_code == status.HTTP_200_OK
        assert user.password_reset_codes.count() == 1
        mock_send.assert_called_once()

    @patch("apps.accounts.views.send_password_reset_email")
    def test_password_reset_nonexistent_email_still_200(self, mock_send, api_client):
        response = api_client.post(self.URL, {"email": "nobody@example.com"})
        assert response.status_code == status.HTTP_200_OK
        mock_send.assert_not_called()


# ── Password Reset Confirm ───────────────────────────────────────────


@pytest.mark.django_db
class TestPasswordResetConfirmView:
    URL = "/api/auth/password-reset-confirm/"

    def test_password_reset_confirm_changes_password(self, api_client):
        user = UserFactory()
        code = PasswordResetCodeFactory(user=user)
        data = {
            "email": user.email,
            "code": code.code,
            "new_password": "newStrong!1",
            "new_password_confirm": "newStrong!1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.check_password("newStrong!1")
        code.refresh_from_db()
        assert code.used_at is not None

    def test_password_reset_confirm_invalid_code_400(self, api_client):
        user = UserFactory()
        PasswordResetCodeFactory(user=user)
        data = {
            "email": user.email,
            "code": "000000",
            "new_password": "newStrong!1",
            "new_password_confirm": "newStrong!1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ── Password Change ──────────────────────────────────────────────────


@pytest.mark.django_db
class TestPasswordChangeView:
    URL = "/api/auth/password-change/"

    def test_password_change_success(self, api_client):
        user = UserFactory()
        api_client.force_authenticate(user=user)
        data = {
            "current_password": "testpass123",
            "new_password": "newStrong!1",
            "new_password_confirm": "newStrong!1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.check_password("newStrong!1")

    def test_password_change_keeps_current_session(self, api_client):
        UserFactory(email="change@example.com")
        api_client.post(
            "/api/auth/login/",
            {"email": "change@example.com", "password": "testpass123"},
        )
        data = {
            "current_password": "testpass123",
            "new_password": "newStrong!1",
            "new_password_confirm": "newStrong!1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_200_OK
        # Session should still be valid after password change
        me_response = api_client.get("/api/auth/me/")
        assert me_response.status_code == status.HTTP_200_OK

    def test_password_change_wrong_current_password_400(self, api_client):
        user = UserFactory()
        api_client.force_authenticate(user=user)
        data = {
            "current_password": "wrongpassword",
            "new_password": "newStrong!1",
            "new_password_confirm": "newStrong!1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_change_unauthenticated_403(self, api_client):
        data = {
            "current_password": "old",
            "new_password": "newStrong!1",
            "new_password_confirm": "newStrong!1",
        }
        response = api_client.post(self.URL, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


# ── CSRF ─────────────────────────────────────────────────────────────


@pytest.mark.django_db
class TestCSRFView:
    URL = "/api/auth/csrf/"

    def test_csrf_endpoint_sets_cookie(self, api_client):
        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        assert "csrftoken" in response.cookies
