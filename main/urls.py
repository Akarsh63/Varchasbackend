from django.urls import path
from .views import OurTeamViewSet, payment,IndexView
from django.conf.urls import  include
from django.urls import re_path
# app_name = 'main'
urlpatterns = [
    path('payment', payment, name='payment'),
    path('mainapi/', OurTeamViewSet.as_view(), name='teams'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('', IndexView.as_view(), name='home'),
    re_path(r'^', include('adminportal.urls',namespace='adminportal'),name='adminportal'),
]

