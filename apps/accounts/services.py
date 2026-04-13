from __future__ import annotations

import resend
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def send_verification_email(user: User, code: str) -> None:
    """Send a 6-digit email verification code via Resend."""
    resend.Emails.send(
        {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [user.email],
            "subject": "Verifique seu email",
            "html": (
                f"<p>Seu codigo de verificacao e: <strong>{code}</strong></p>"
                f"<p>Este codigo expira em 15 minutos.</p>"
            ),
        }
    )


def send_password_reset_email(user: User, code: str) -> None:
    """Send a 6-digit password reset code via Resend."""
    resend.Emails.send(
        {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [user.email],
            "subject": "Redefinicao de senha",
            "html": (
                f"<p>Codigo para redefinir senha: <strong>{code}</strong></p>"
                f"<p>Este codigo expira em 30 minutos.</p>"
            ),
        }
    )
