from __future__ import annotations

from unittest.mock import patch

import pytest

from apps.accounts.factories import UserFactory
from apps.accounts.services import send_password_reset_email, send_verification_email


@pytest.mark.django_db
class TestSendVerificationEmail:
    @patch("apps.accounts.services.resend.Emails.send")
    def test_calls_resend_with_correct_params(self, mock_send):
        user = UserFactory(email="verify@example.com")
        send_verification_email(user, "123456")

        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args[0][0]
        assert call_kwargs["to"] == ["verify@example.com"]
        assert "123456" in call_kwargs["html"]

    @patch("apps.accounts.services.resend.Emails.send")
    def test_uses_configured_from_email(self, mock_send, settings):
        settings.DEFAULT_FROM_EMAIL = "test@myapp.com"
        user = UserFactory()
        send_verification_email(user, "654321")

        call_kwargs = mock_send.call_args[0][0]
        assert call_kwargs["from"] == "test@myapp.com"


@pytest.mark.django_db
class TestSendPasswordResetEmail:
    @patch("apps.accounts.services.resend.Emails.send")
    def test_calls_resend_with_correct_params(self, mock_send):
        user = UserFactory(email="reset@example.com")
        send_password_reset_email(user, "789012")

        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args[0][0]
        assert call_kwargs["to"] == ["reset@example.com"]
        assert "789012" in call_kwargs["html"]

    @patch("apps.accounts.services.resend.Emails.send")
    def test_subject_mentions_password(self, mock_send):
        user = UserFactory()
        send_password_reset_email(user, "111111")

        call_kwargs = mock_send.call_args[0][0]
        subject = call_kwargs["subject"].lower()
        assert "senha" in subject or "password" in subject
