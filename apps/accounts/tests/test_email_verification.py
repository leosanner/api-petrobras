from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.accounts.models import EmailVerification

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="verify@example.com",
        username="verify",
        password="s3cret!",
    )


@pytest.mark.django_db
class TestEmailVerification:
    def test_code_has_six_digits(self, user):
        verification = EmailVerification.objects.create(user=user)
        assert len(verification.code) == 6
        assert verification.code.isdigit()

    def test_expires_at_is_after_created_at_by_expiration_minutes(self, user):
        verification = EmailVerification.objects.create(user=user)
        delta = verification.expires_at - verification.created_at
        expected = timedelta(minutes=EmailVerification.EXPIRATION_MINUTES)
        # Allow small timing tolerance (up to 2 seconds)
        assert abs((delta - expected).total_seconds()) < 2

    def test_is_valid_when_not_used_and_not_expired(self, user):
        verification = EmailVerification.objects.create(user=user)
        assert verification.is_valid() is True

    def test_is_invalid_when_expired(self, user):
        verification = EmailVerification.objects.create(user=user)
        verification.expires_at = timezone.now() - timedelta(seconds=1)
        verification.save(update_fields=["expires_at"])
        assert verification.is_valid() is False

    def test_is_invalid_when_already_used(self, user):
        verification = EmailVerification.objects.create(user=user)
        verification.mark_used()
        assert verification.is_valid() is False

    def test_mark_used_sets_used_at(self, user):
        verification = EmailVerification.objects.create(user=user)
        assert verification.used_at is None
        before = timezone.now()
        verification.mark_used()
        after = timezone.now()
        assert verification.used_at is not None
        assert before <= verification.used_at <= after

    def test_user_can_have_multiple_verifications(self, user):
        v1 = EmailVerification.objects.create(user=user)
        v2 = EmailVerification.objects.create(user=user)
        assert v1.pk != v2.pk
        assert user.email_verifications.count() == 2

    def test_deleting_user_cascades_to_verifications(self, user):
        EmailVerification.objects.create(user=user)
        EmailVerification.objects.create(user=user)
        user_id = user.pk
        user.delete()
        assert EmailVerification.objects.filter(user_id=user_id).count() == 0
