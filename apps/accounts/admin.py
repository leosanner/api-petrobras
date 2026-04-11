from django.contrib import admin

from apps.accounts.models import EmailVerification, User

admin.site.register(User)
admin.site.register(EmailVerification)
