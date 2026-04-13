from django.contrib import admin

from apps.accounts.models import EmailVerification, PasswordResetCode, User

admin.site.register(User)
admin.site.register(EmailVerification)
admin.site.register(PasswordResetCode)
