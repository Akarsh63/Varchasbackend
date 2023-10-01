from .views import RegisterView, DisplayProfile, joinTeam, DisplayTeam, leaveTeam, UserViewSet, GroupViewSet, EsportsRegisterViewValorant, EsportsRegisterViewBGMI, EsportsRegisterViewChess, EsportsRegisterView, getAthleticEvents, getBadmintonEvents, getBasketBallEvents, getTableTennisEvents, getVolleyBallEvents
from django.urls import path, include
from rest_framework import routers
from .views import LoginUserView,RegisterUserView,HomeView,userleaveTeam,userjoinTeam,userDisplayteam,userDisplayProfile
from django.urls import re_path 
app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', RegisterView.as_view(), name='register'),
    path('userregister/',RegisterUserView.as_view(),name='userregister'),
    path('userlogin/',LoginUserView,name='userlogin'),
    path('userinfo/',HomeView.as_view(),name='userinfo'),
    re_path('profile', DisplayProfile, name='profile'),
    path('EsportsRegister/', EsportsRegisterView, name='EsportsRegister'),
    path('EsportsRegister/Valorant/', EsportsRegisterViewValorant.as_view(), name='EsportsRegisterValorant'),
    path('EsportsRegister/BGMI/', EsportsRegisterViewBGMI.as_view(), name='EsportsRegisterBGMI'),
    path('EsportsRegister/Chess/', EsportsRegisterViewChess.as_view(), name='EsportsRegisterChess'),
    re_path('myTeam', DisplayTeam, name='myTeam'),
    re_path('joinTeam', joinTeam, name='joinTeam'),
    re_path('leaveTeam', leaveTeam, name='leaveTeam'),
    path('jointeam/', userjoinTeam, name='userjoinTeam'),
    path('leaveteam/', userleaveTeam, name='userleaveTeam'),
    path('displayTeam/',userDisplayteam,name='userDisplayteam'),
    path('displayProfile/',userDisplayProfile,name='userDisplayprofile'),
    path('athletics/', getAthleticEvents, name='athleticEvents'),
    path('badminton/', getBadmintonEvents, name='badmintonEvents'),
    path('tabletennis/', getTableTennisEvents, name='tabletennisEvents'),
    path('voleyball/', getVolleyBallEvents, name='volleyballEvents'),
    path('basketball/', getBasketBallEvents, name='basketballEvents'),
]
