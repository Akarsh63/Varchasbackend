from django.contrib import admin
from .models import TeamRegistration, EsportsTeamRegistration


class TeamAdmin(admin.ModelAdmin):
    class Meta:
        model = TeamRegistration


class EsportsTeamAdmin(admin.ModelAdmin):
    class Meta:
        model = EsportsTeamRegistration


admin.site.register(TeamRegistration, TeamAdmin)
admin.site.register(EsportsTeamRegistration, EsportsTeamAdmin)
