from __future__ import annotations

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.accounts.models import PasswordResetCode

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="reset@example.com",
        username="resetuser",
        password="s3cret!",
    )


@pytest.mark.django_db
class TestPasswordResetCode:
    def test_code_has_six_digits(self, user):
        code = PasswordResetCode.objects.create(user=user)
        assert len(code.code) == 6
        assert code.code.isdigit()

    def test_expiration_minutes_is_30(self):
        assert PasswordResetCode.EXPIRATION_MINUTES == 30

    def test_expires_at_uses_own_expiration_minutes(self, user):
        code = PasswordResetCode.objects.create(user=user)
        delta = code.expires_at - code.created_at
        expected = timedelta(minutes=PasswordResetCode.EXPIRATION_MINUTES)
        assert abs((delta - expected).total_seconds()) < 2

    def test_is_valid_when_not_used_and_not_expired(self, user):
        code = PasswordResetCode.objects.create(user=user)
        assert code.is_valid() is True

    def test_is_invalid_when_expired(self, user):
        code = PasswordResetCode.objects.create(user=user)
        code.expires_at = timezone.now() - timedelta(seconds=1)
        code.save(update_fields=["expires_at"])
        assert code.is_valid() is False

    def test_is_invalid_when_already_used(self, user):
        code = PasswordResetCode.objects.create(user=user)
        code.mark_used()
        assert code.is_valid() is False

    def test_mark_used_sets_used_at(self, user):
        code = PasswordResetCode.objects.create(user=user)
        assert code.used_at is None
        before = timezone.now()
        code.mark_used()
        after = timezone.now()
        assert code.used_at is not None
        assert before <= code.used_at <= after

    def test_user_can_have_multiple_reset_codes(self, user):
        c1 = PasswordResetCode.objects.create(user=user)
        c2 = PasswordResetCode.objects.create(user=user)
        assert c1.pk != c2.pk
        assert user.password_reset_codes.count() == 2

    def test_deleting_user_cascades_to_reset_codes(self, user):
        PasswordResetCode.objects.create(user=user)
        PasswordResetCode.objects.create(user=user)
        user_id = user.pk
        user.delete()
        assert PasswordResetCode.objects.filter(user_id=user_id).count() == 0
