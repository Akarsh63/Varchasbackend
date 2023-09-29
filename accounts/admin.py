from django.contrib import admin
from .models import UserProfile, EsportsUserProfile


class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile


class EsportsUserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = EsportsUserProfile


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EsportsUserProfile, EsportsUserProfileAdmin)
