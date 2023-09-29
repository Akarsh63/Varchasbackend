from django.urls import path, include
from rest_framework import routers
from .views import SponsorView, SponsorViewSet

app_name = 'sponsor'

router = routers.DefaultRouter()
router.register(r'sponsor', SponsorViewSet)

urlpatterns = [
    path('', SponsorView.as_view(), name='index'),
    path('sponsorapi/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
