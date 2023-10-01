from .views import TeamFormationView, removePlayerView, TeamViewSet,removeplayer,CreateTeamView
from rest_framework import routers
from django.urls import path, include

app_name = 'registration'
router = routers.DefaultRouter()
router.register('teamsApi', TeamViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('team', TeamFormationView.as_view(), name='team'),
    path('removePlayer', removePlayerView.as_view(), name='remove_player'),
    path('removeplayer/',removeplayer,name='removeplayer'),
    path('createteam/',CreateTeamView,name='CreateTeamView')
    # url(r'team/(?P<username>[a-zA-Z0-9]+)$',TeamFormationView),
]
