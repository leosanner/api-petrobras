from __future__ import annotations

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import EmailVerification, PasswordResetCode
from apps.accounts.serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
    VerifyEmailSerializer,
)
from apps.accounts.services import send_password_reset_email, send_verification_email

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            email=serializer.validated_data["email"],
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
            is_active=False,
        )

        verification = EmailVerification.objects.create(user=user)
        send_verification_email(user, verification.code)

        return Response(
            {"detail": "Registration successful. Check your email."},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        verification = serializer.validated_data["verification"]

        verification.mark_used()
        user.is_active = True
        user.save(update_fields=["is_active"])

        return Response({"detail": "Email verified successfully."})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_active:
            return Response(
                {"detail": "Account is not active. Please verify your email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        logout(request)
        return Response({"detail": "Logged out successfully."})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(UserSerializer(request.user).data)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data["email"])
        except User.DoesNotExist:
            return Response(
                {"detail": "If the email exists, a reset code has been sent."}
            )

        reset_code = PasswordResetCode.objects.create(user=user)
        send_password_reset_email(user, reset_code.code)

        return Response({"detail": "If the email exists, a reset code has been sent."})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid email or code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reset_code = (
            PasswordResetCode.objects.filter(user=user, code=code)
            .order_by("-created_at")
            .first()
        )

        if reset_code is None or not reset_code.is_valid():
            return Response(
                {"detail": "Invalid email or code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reset_code.mark_used()
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        return Response({"detail": "Password reset successfully."})


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.check_password(
            serializer.validated_data["current_password"]
        ):
            return Response(
                {"detail": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password"])
        update_session_auth_hash(request, request.user)

        return Response({"detail": "Password changed successfully."})


class CSRFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        get_token(request)
        return Response({"detail": "CSRF cookie set."})
