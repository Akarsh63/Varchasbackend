import smtplib
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from .models import TeamRegistration
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import TeamsSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTeamView(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    sport = request.data['sport']
    if sport is None or sport == '':
        return Response({"message": "Sport field is required"}, status=status.HTTP_400_BAD_REQUEST)
    sport_info = int(sport)
    if user_profile.teamId.exists():
        if sport_info in [1,2,3,4,5,6,7,8,9,10,11,12] :
            teams=user_profile.teamId.all()
            for team in teams:
                if int(team.sport) in [1,2,3,4,5,6,7,8,9,10,11,12] :
                    message = "You are not able to create the team. \nOnly one team can be created per user. \nYou can join team cerated by your team captain"
                    message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                    return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
        if sport_info in [13,14,15]:
            teams=user_profile.teamId.all()
            for team in teams:
                if int(team.sport) == sport_info :
                    message = "You are not able to create the team. \nOnly one team can be created per user. \nYou can join team cerated by your team captain"
                    message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                    return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
    requested_data = {
        "sport": sport_info,
        "category": request.data['category'],
        "teamsize": request.data['teamsize'],
    }
    serializer = TeamsSerializer(data=requested_data)
    if serializer.is_valid():
        category = serializer.validated_data['category']
        teamsize = serializer.validated_data['teamsize']
        sport = serializer.validated_data['sport']
        spor = TeamRegistration.SPORT_CHOICES[int(sport)-1][1][:3]
        teams_data = request.data.get('teams', [])
        for team_name in teams_data:
            team_id = "VA-{}-{}-{}-{}".format(spor[:3].upper(), user.username[:3].upper(),randint(1, 99), randint(1, 9))
            team = TeamRegistration.objects.create(
                teamId=team_id,
                sport=sport,
                college=user_profile.college,
                captian=user_profile,
                score=-1,
                category=category,
                teamsize=teamsize,
                teamcount=1,
                teams=team_name
            )
            user1=request.user
            subject='Varchas23 | Confirmation of Team registration'
            event_name = f"{TeamRegistration.SPORT_CHOICES[int(sport) - 1][1]} {team_name}"
            participant_name = user1.first_name
            team_id = team_id
            message = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                        </head>
                        <body>
                            <div class="container">
                                <div class="content">
                                    <p>Hi {participant_name},</p>
                                    <p>This is a confirmation email regarding your successful registration for {event_name}.</p>
                                    <p><b>Name of participant: {participant_name}</b></p>
                                    <p><b>Event: {event_name}</b></p>
                                    <p><b>Team Id: {team_id}</b></p>
                                    <p style="color:grey">Don't reply to this email. For any queries, contact Varchas'23 team or visit <a href="https://varchas23.in">varchas23.in</a></p>
                                    <p>Thank you for being part of Varchas'23</p>
                                    <p style="color:grey"><b><i>Thanks and Regards,<br>Festival Chiefs Varchas'23<br>IIT Jodhpur</i></b></p>
                                </div>
                            </div>
                        </body>
                        </html>
                        """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user1.email,]
            # try:
            #     connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            #     connection.starttls()  # Use TLS
            #     connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            #     connection.sendmail(email_from, recipient_list,f'Subject: {subject}\nContent-Type: text/html; charset=utf-8\n\n{message}')
            #     connection.quit()
            #     print("Email sent successfully")
            # except Exception as e:
            #     print(f"Email could not be sent. Error: {str(e)}")
            user_profile.teamId.add(team)
            if sport_info in [13, 15]:
                    team.teamcount = team.teamsize
                    team.save()
                    if sport_info == 13:
                        user_profile.team_member1_bgmi_ingame_id = request.data.get('team_id', {}).get('id1')
                        user_profile.team_member2_bgmi_ingame_id = request.data.get('team_id', {}).get('id2')
                        user_profile.team_member3_bgmi_ingame_id = request.data.get('team_id', {}).get('id3')
                        user_profile.team_member4_bgmi_ingame_id = request.data.get('team_id', {}).get('id4')
                    if sport_info == 14:
                        user_profile.team_member1_val_ingame_id = request.data.get('team_id', {}).get('id1')
                        user_profile.team_member2_val_ingame_id = request.data.get('team_id', {}).get('id2')
                        user_profile.team_member3_val_ingame_id = request.data.get('team_id', {}).get('id3')
                        user_profile.team_member4_val_ingame_id = request.data.get('team_id', {}).get('id4')
                        user_profile.team_member5_val_ingame_id = request.data.get('team_id', {}).get('id5')
                    if sport_info ==15 :
                        user_profile.team_member1_cr_ingame_id =request.data.get('team_id', {}).get('id1')


                    user_profile.isesports = True
                
            user_profile.save()
            print(user_profile)
        return Response({"message": "Team(s) created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removeplayer(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    team_id = user_profile.teamId

    if user_profile.teamId is None:
        return Response({"message": "You must be registered in a team to complete this operation."},
                        status=status.HTTP_400_BAD_REQUEST)

    team = TeamRegistration.objects.get(teamId=team_id)
    if user_profile != team.captian:
        return Response({"message": "Only the captain can remove a player from the team."},
                        status=status.HTTP_401_UNAUTHORIZED)

    user_to_remove_id = request.data.get('user')
    user_to_remove = User.objects.filter(id=user_to_remove_id).first()  # Get the User object
    
    if user_to_remove is None:
        return Response({"message": "The specified user does not exist."},
                        status=status.HTTP_400_BAD_REQUEST)

    player_to_remove = UserProfile.objects.filter(user=user_to_remove).first()  # Get the associated UserProfile
    
    if player_to_remove is None:
        return Response({"message": "The specified user is not in the team."},
                        status=status.HTTP_400_BAD_REQUEST)
    if user_profile == player_to_remove:
        return Response({"message": "You can not remove your self"},
                        status=status.HTTP_400_BAD_REQUEST)

    player_to_remove.teamId = None
    player_to_remove.save()
    team.teamcount=team.teamcount-1
    team.save()
    return Response({"message": "Player removed from the team successfully."},
                    status=status.HTTP_200_OK)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = TeamRegistration.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
