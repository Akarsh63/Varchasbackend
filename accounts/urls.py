from .views import UserViewSet, GroupViewSet
from django.urls import path, include
from rest_framework import routers
from .views import LoginUserView,RegisterUserView,userleaveTeam,userjoinTeam,userDisplayteam,userDisplayProfile,PasswordReset,OTPVerification,restpassword,resendpassword,noprofile,deleteusers
app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('userregister/',RegisterUserView.as_view(),name='userregister'),
    path('userlogin/',LoginUserView,name='userlogin'),
    path('jointeam/', userjoinTeam, name='userjoinTeam'),
    path('leaveteam/', userleaveTeam, name='userleaveTeam'),
    path('displayTeam/',userDisplayteam,name='userDisplayteam'),
    path('displayProfile/',userDisplayProfile,name='userDisplayprofile'),
    path('password_reset_request/',PasswordReset.as_view(),name='passwordrequest'),
    path('otp_verification/',OTPVerification.as_view(),name='otpverification'),
    path('reset_password/',restpassword,name='restpassword'),
    path('resendpassword/',resendpassword,name='resendpassword'),
    path('noprofile/',noprofile,name='noprofile'),
    path('deleteusers/',deleteusers,name='deleteusers'),
]
