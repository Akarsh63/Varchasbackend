from django.urls import path
from .views import dashboardTeams, dashboardEsportsTeams
from .views import dashboardUsers, dashboard, downloadExcel, sendMail, updateScore, downloadEsportsExcel
# from django.conf.urls import url

app_name = 'adminportal'

urlpatterns = [
    path('mail', sendMail.as_view(), name='mail'),
    path(r'teamsEsports$', dashboardEsportsTeams, name='deteams'),
    path(r'updateScore/(<str:sport>)/', updateScore, name='uscore'),
    path(r'teams$', dashboardTeams, name='dteams'),
    path(r'users$', dashboardUsers, name='dusers'),
    path(r'excel$', downloadExcel, name='teamInfo'),
    path(r'excelEsports$', downloadEsportsExcel, name='esportsInfo'),
    path('', dashboard, name='dashboard'),
]
