from django.contrib import admin
from .models import UserProfile, EsportsUserProfile,PasswordResetRequest


class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile


class EsportsUserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = EsportsUserProfile

class OTPAdmin(admin.ModelAdmin):
    class Meta:
        model=PasswordResetRequest

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EsportsUserProfile, EsportsUserProfileAdmin)
admin.site.register(PasswordResetRequest,OTPAdmin)