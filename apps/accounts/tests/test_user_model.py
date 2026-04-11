import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_with_email_and_password(self):
        user = User.objects.create_user(
            email="alice@example.com",
            username="alice",
            password="s3cret!",
        )
        assert user.email == "alice@example.com"
        assert user.check_password("s3cret!")
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_email_is_required(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email="", username="bob", password="s3cret!")

    def test_email_is_unique(self):
        User.objects.create_user(
            email="dup@example.com", username="user1", password="s3cret!"
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="dup@example.com", username="user2", password="s3cret!"
            )

    def test_email_is_normalized(self):
        user = User.objects.create_user(
            email="Foo@EXAMPLE.com",
            username="foo",
            password="s3cret!",
        )
        # normalize_email lowercases only the domain part
        assert user.email == "Foo@example.com"

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="root@example.com",
            username="root",
            password="s3cret!",
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.is_active is True

    def test_username_field_is_email(self):
        assert User.USERNAME_FIELD == "email"

    def test_required_fields_contains_username(self):
        assert "username" in User.REQUIRED_FIELDS

    def test_str_returns_email(self):
        user = User.objects.create_user(
            email="stringy@example.com",
            username="stringy",
            password="s3cret!",
        )
        assert str(user) == "stringy@example.com"
