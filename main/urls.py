from django.urls import path
from .views import IndexView, NavBarSubOptionsPageView, OurTeamView, comingSoon, OurTeamViewSet, gallery, payment, paymentCompletion, privacy
from django.conf.urls import  include
from django.urls import re_path 
app_name = 'main'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('OurTeam', OurTeamView.as_view(), name='OurTeam'),
    path('gallery', gallery, name='gallery'),
    path('payment', payment, name='payment'),
    path('paymentCF', paymentCompletion, name='paymentCF'),
    path('privacy', privacy, name='privacy'),
    path('<slug:slug>', NavBarSubOptionsPageView.as_view(),
         name='navbarsuboptionpage'),
    path('mainapi/', OurTeamViewSet.as_view(), name='teams'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^comingSoon$', comingSoon, name='comingSoon'),
]
