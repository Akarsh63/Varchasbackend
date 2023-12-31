import random
from .models import UserProfile,PasswordResetRequest
from django.utils import timezone
from django.shortcuts import get_object_or_404
from registration.models import TeamRegistration
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer,UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
import smtplib
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse, redirect
from django.contrib.auth.hashers import make_password

# api method to register the user 

class RegisterUserView(APIView):
    def post(self, request):
        print(request.data)
        if len(request.data.get('phone')) != 10:
            return Response({"message": "Phone number must be 10 digits"}, status=status.HTTP_400_BAD_REQUEST)
    
        user1 = User.objects.filter(email=request.data.get('email')).first()
        if user1:
            return Response({"message": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('password') != request.data.get('confirm_password'):
            return Response({"message": "Passwords don't match!"}, status=status.HTTP_400_BAD_REQUEST)
        hashed_password = make_password(request.data["password"])
        user_data = {
            "username": request.data["email"],
            "email": request.data["email"],
            "first_name": request.data.get("first_name", ""),
            "last_name": request.data.get("last_name", ""),
            "password": hashed_password,
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            profile_data = {
                "user": user.id,
                "phone": request.data["phone"],
                "gender": request.data["gender"],
                "college": request.data["college"],
                "state": request.data["state"],
                "accommodation_required": request.data["accommodation_required"],
            }
    
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response({"message": 'User created Successfully'}, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response({"message":"Sorry, Please try again!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Sorry, Please try again!"}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# api method to login the user 

@api_view(['POST'])
def LoginUserView(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = User.objects.filter(email=email).first()
    
    if user is None:
        return Response({"message": 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(password):
        return Response({"message": 'Invalid Password or Email'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a JWT token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)  # Extract the refresh token value

    return Response({"message": 'User Logged in Successfully!', "access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return reverse('adminportal:dashboard')
        # else:
        #     return reverse('main:home')

class PasswordReset(APIView):
    def post(self,request):
         email = request.data.get('email')
         user=get_object_or_404(User,email=email)
         if not user:
             return Response({"message":"Sorry! User not found"},status=status.HTTP_404_NOT_FOUND)
         otp = random.randint(1000, 9999)
         try :
             reset_request=PasswordResetRequest.objects.get(email=email)
             reset_request.otp=otp
             reset_request.save()
         except:
            reset_request = PasswordResetRequest(user=user,email=email,otp=otp)
            reset_request.save()
         subject='Varchas23 | OTP Verification'
         message = f'Hi {user.username}, Here is your otp {otp}.'
         email_from=settings.EMAIL_HOST_USER
         recipient_list = [user.email, ]
         try:
            connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            connection.starttls()  # Use TLS
            connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            connection.sendmail(email_from, recipient_list, f'Subject: {subject}\n\n{message}')
            connection.quit()
            print("Email sent successfully")
         except Exception as e:
            print(f"Email could not be sent. Error: {str(e)}")
         return Response({"message":"OTP sent Successfully!"},status=status.HTTP_201_CREATED)         

class OTPVerification(APIView):
    def post(self, request):
        email_req = request.data['email']
        otp = request.data.get('otp')

        try:
            reset_request =PasswordResetRequest.objects.filter(email=email_req).first()
        except PasswordResetRequest.DoesNotExist:
            return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)
        if reset_request.expiration_time < timezone.now():
            return Response({"message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_request.otp != int(otp):
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def resendpassword(request):
    email_req=request.data.get('email')
    user=get_object_or_404(User,email=email_req)
    if not user:
        return Response({"message":"Sorry! User not found"},status=status.HTTP_404_NOT_FOUND)
    try:
        reset_request=PasswordResetRequest.objects.get(email=email_req)
    except:
        return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)     
    otp = random.randint(1000, 9999)
    reset_request.otp=otp
    reset_request.save()
    subject='Varchas23 | OTP Verification'
    message = f'Hi {user.username}, Here is your otp {otp}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    try:
        print(1)
        connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(2)
        connection.starttls()  # Use TLS
        print(3)
        connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print(4)
        connection.sendmail(email_from, recipient_list, f'Subject: {subject}\n\n{message}')
        print(5)
        connection.quit()
        print(6)
        print("Email sent successfully")
    except Exception as e:
        print(7)
        print(f"Email could not be sent. Error: {str(e)}")
    return Response({"message":"OTP sent Successfully!"},status=status.HTTP_201_CREATED) 

@api_view(['POST'])
def restpassword(request):
    email_req=request.data.get('email')
    password=request.data.get('password')
    try:
        user=User.objects.get(email=email_req)
    except:
        return Response({"message":"Sorry! User not found"},status=status.HTTP_404_NOT_FOUND)
    user.set_password(password)
    user.save()
    return Response({"message":"Successfully changed password"},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userleaveTeam(request):
    user = get_object_or_404(UserProfile, user=request.user)
    teamId = user.teamId
    team = get_object_or_404(TeamRegistration, teamId=teamId)
    user.teamId = None
    user.save()
    team.delete()
    return Response({"message": "You have left the team successfully."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userjoinTeam(request):
    user = request.user
    teamId = request.data.get('teamId')
    if user is not None:
        user = get_object_or_404(UserProfile, user=user)
        team = get_object_or_404(TeamRegistration, teamId=teamId)
        sport = team.sport
        sport_info = int(sport) 
        if user.teamId.exists():
            if sport_info in [1,2,3,4,5,6,7,8,9,10,11,12] :
                teams=user.teamId.all()
                for team in teams:
                    if int(team.sport) in [3,4,5,6,7,8,9,10,11,12] :
                            message = "You are not able to join the team. \nOnly one team can be joined per user."
                            message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                            return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    if int(team.sport) ==1 :
                          if sport_info!=1:
                            message = "You are not able to join the team. \nOnly one team can be joined per user."
                            message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                            return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
                          teamdata=TeamRegistration.objects.get(teamId=teamId)
                          if sport_info ==1 and teamdata.category==team.category and teamdata.teams==team.teams:
                            message = "You are not able to join the team. \nOnly one team can be joined per user."
                            message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                            return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    if int(team.sport) ==2:
                          if sport_info!=2:
                            message = "You are not able to join the team. \nOnly one team can be joined per user."
                            message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                            return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
                          teamdata=TeamRegistration.objects.get(teamId=teamId)
                          if sport_info ==2 and teamdata.category==team.category:
                            message = "You are not able to join the team. \nOnly one team can be joined per user."
                            message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                            return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    
            if sport_info in [13,14,15]:
                teams=user.teamId.all()
                for team in teams:
                    if int(team.sport) == sport_info :
                         message = "You are not able to join the team. \nOnly one team can be joined per user."
                         message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                         return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # if user.gender != team.captian.gender:
        #     return Response({"message":"Sorry,Gender not matched!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        team = get_object_or_404(TeamRegistration, teamId=teamId)
        if(int(team.teamcount) < int(team.teamsize)):
            user.teamId.add(team)
            user.save()
            team.teamcount=team.teamcount+1
            team.save()
            return Response({"message": "Joined team Successfully!"}, status=status.HTTP_201_CREATED)
        else:
           return Response({"message":"Sorry,Team size exceeded!"},status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response({"message": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDisplayteam(request):
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        team_data = []
        if user_profile.teamId.exists():
            teams = user_profile.teamId.all()
            for team in teams:
                if int(team.sport)==13:
                    team_users_info=[
                        {"Player1_id":user_profile.team_member1_bgmi_ingame_id},
                        {"Player2_id":user_profile.team_member2_bgmi_ingame_id},
                        {"Player3_id":user_profile.team_member3_bgmi_ingame_id},
                        {"Player4_id":user_profile.team_member4_bgmi_ingame_id}]
                elif int(team.sport)==14:
                    team_users_info=[
                        {"Player1_id":user_profile.team_member1_val_ingame_id},
                        {"Player2_id":user_profile.team_member2_val_ingame_id},
                        {"Player3_id":user_profile.team_member3_val_ingame_id},
                        {"Player4_id":user_profile.team_member4_val_ingame_id},
                        {"Player5_id":user_profile.team_member5_val_ingame_id}
                    ]
                elif int(team.sport)==15:
                    team_users_info=[
                        {"Player_id":user_profile.team_member1_cr_ingame_id}
                    ]
                else:
                    team_users_info = [
                        {
                            "user_id": user_data.user.id,
                            "email": user_data.user.username,
                            "phone": user_data.phone,
                            "name": user_data.user.first_name + user_data.user.last_name
                        }
                        for user_data in UserProfile.objects.filter(teamId=team)
                    ]
                team_info = {
                    "event":team.teams,
                    "team_id": team.teamId,
                    "sport": team.sport,
                    "college": team.college,
                    "captain_username": team.captian.user.first_name + team.captian.user.last_name if team.captian else None,
                    "score": team.score,
                    "category": team.category,
                    "players_info":team_users_info,
                    "captain": team.captian==user_profile
                }
                
                team_data.append(team_info)
        
        if not team_data:
            return Response({"message": "Join a team"}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            "team_data": team_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDisplayProfile(request):
    print(1)
    print(request.user)
    try:
       user = get_object_or_404(UserProfile, user=request.user)
    except UserProfile.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    print(user)
    if user is None:
        return Response({"message":"User not found!"},status=status.HTTP_404_NOT_FOUND)
    response_data = {
                "team_id": [team.teamId for team in user.teamId.all()] if user.teamId.exists() else None,
                "college": user.college,
                "user_id": user.user.id,
                "email": user.user.username,
                "phone": user.phone,
                "name":user.user.first_name +user.user.last_name
         }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def noprofile(request):
    users = User.objects.all()
    userprofiles = UserProfile.objects.all()
    data = []
    
    for user in users:  
        try:
            userprof = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            data.append(user.username)
    message={"users": users.count(), "profiles": userprofiles.count(), "userswithnoprofile": data,"count":len(data)}
    return Response(message, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteusers(request):
    data = request.data.get("users", []) 
    for username in data:
        try:
            user_to_delete = User.objects.get(username=username)
            user_to_delete.delete()
        except User.DoesNotExist:
             pass 
    return Response("Operation completed", status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
