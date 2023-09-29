from .views import BadmintonViewSet, CreateMatch, CricketViewSet, FootballViewSet, TTViewSet, TennisViewSet, VolleyballViewSet, ChessViewSet, SquashViewSet, BasketballViewSet, MatchViewSet, TT, badminton, cricket, squash, football, volleyball, chess, athletics, informals, tennis, basketball, valorant, bgmi, fixtures, kabaddi, weightlifting
from django.urls import path, include
from rest_framework import routers

app_name = 'events'

router = routers.DefaultRouter()
router.register(r'cricketApi', CricketViewSet)
router.register(r'footballApi', FootballViewSet)
router.register(r'volleyballApi', VolleyballViewSet)
router.register(r'chessApi', ChessViewSet)
router.register(r'squashApi', SquashViewSet)
router.register(r'TTApi', TTViewSet)
router.register(r'badmintonApi', BadmintonViewSet)
router.register(r'TennisApi', TennisViewSet)
router.register(r'basketballApi', BasketballViewSet)
router.register(r'MatchApi', MatchViewSet)

urlpatterns = [
    path('add', CreateMatch.as_view(), name='add_match'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('cricket', cricket, name='cricket'),
    path('football', football, name='football'),
    path('volleyball', volleyball, name='volleyball'),
    path('chess', chess, name='chess'),
    path('TT', TT, name='TT'),
    path('badminton', badminton, name='badminton'),
    path('tennis', tennis, name='tennis'),
    path('athletics', athletics, name='athletics'),
    path('informals', informals, name='informals'),
    path('basketball', basketball, name='basketball'),
    path('valorant', valorant, name='valorant'),
    path('bgmi', bgmi, name='bgmi'),
    path('kabaddi', kabaddi, name='kabaddi'),
    path('squash', squash, name='squash'),
    path('weightlifting', weightlifting, name='weightlifting'),
    path('fixtures/(<str:sport>)/', fixtures, name='fixtures'),
]
