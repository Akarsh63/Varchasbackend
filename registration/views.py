from django.views.generic import CreateView
from .forms import TeamRegistrationForm, RemovePlayerForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from django.http import HttpResponse
from random import random
from .models import TeamRegistration
from django.core.mail import send_mail
from django.views.generic import FormView
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import TeamsSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status
from random import randint

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTeamView(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.teamId is not None:
                message = "You are already in team {}".format(user_profile.teamId)
                message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)
    sport = request.data['sport']
    sport_info = int(sport) 
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
        team_id = "VA-{}-{}-{}".format(spor[:3].upper(), user.username[:3].upper(), randint(1, 999))
        teams_data = request.data.get('teams', [])
        team = TeamRegistration.objects.create(
            teamId=team_id,
            sport=sport,
            college=user_profile.college,
            captian=user_profile,
            score=-1,
            category=category,
            teamsize=teamsize,
            teamcount=1,
            teams=teams_data
        )
        user_profile.teamId = team
        if sport_info in [13, 15]:
            team.teamcount=team.teamsize
            team.save()
            user_profile.team_member1_ingame_id = request.data.get('team_member1_ingame_id')
            if sport_info == 13:
                user_profile.team_member2_ingame_id = request.data.get('team_member2_ingame_id')
                user_profile.team_member3_ingame_id = request.data.get('team_member3_ingame_id')
                user_profile.team_member4_ingame_id = request.data.get('team_member4_ingame_id')
            if sport_info == 14:
                user_profile.team_member2_ingame_id = request.data.get('team_member2_ingame_id')
                user_profile.team_member3_ingame_id = request.data.get('team_member3_ingame_id')
                user_profile.team_member4_ingame_id = request.data.get('team_member4_ingame_id')
                user_profile.team_member5_ingame_id = request.data.get('team_member5_ingame_id')
            user_profile.isesports=True
        user_profile.save()
        return Response({"message": "Team created successfully.", "team_id": team.teamId}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamFormationView(CreateView):
    form_class = TeamRegistrationForm
    template_name = 'registration/team.html'
    success_url = '/account/myTeam'

    def form_valid(self, form):
        user = self.request.user
        if user is not None:
            form = TeamRegistrationForm(self.request.POST)
            user = get_object_or_404(UserProfile, user=user)
            if user.teamId is not None:
                message = "You are already in team {}".format(user.teamId)
                message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                return HttpResponse(message, content_type="text/plain")
            team = form.save()
            # if team.sport == '5':
            #     message = "Registration for Cricket has been closed."
            #     team.delete()
            #     return HttpResponse(message, content_type="text/plain")
            # if ((team.sport == '3' or team.sport == '9') and user.gender == 'M'):
            #     message = "Registration for Volleyball(M) and basketball(M) has been closed."
            #     team.delete()
            #     return HttpResponse(message, content_type="text/plain")
            # if team.sport == '6':
            #     message = "Registration for Football has been closed."
            #     team.delete()
            #     return HttpResponse(message, content_type="text/plain")
            # if team.sport == '4':
            #     message = "Registration for Chess will reopen soon."
            #     team.delete()
            #     return HttpResponse(message, content_type="text/plain")
            spor = TeamRegistration.SPORT_CHOICES[int(team.sport)-1][1][:3]
            team.teamId = "VA-" + spor[:3].upper() + '-' + user.user.username[:3].upper() + "{}".format(int(random()*100))
            team.captian = user
            team.save()
            user.teamId = team
            user.save()

            message = '''<!DOCTYPE html> <html><body>Hi {}!<br>You have successfully registered for Varchas2022.<br>Your teamId is: <b>{}</b><br>
                          Check your team details here: <a href="http://varchas22.in/account/myTeam">varchas22.in/account/myTeam</a><p>Vigour| Valour| Victory.</p></body></html>'''.format(user.user.first_name, user.teamId)
            send_mail('Varchas Team Created', message, 'noreply@varchas22.in', [team.captian.user.email],fail_silently=False, html_message=message)

            return super(TeamFormationView, self).form_valid(form)
        return HttpResponse("404")

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


# @login_required(login_url="login")
class removePlayerView(FormView):
    form_class = RemovePlayerForm
    template_name = 'registration/remove_player.html'
    success_url = '/account/myTeam'

    def form_valid(self, form):
        user = get_object_or_404(UserProfile, user=self.request.user)
        teamId = user.teamId
        if user.teamId is None:
            return HttpResponse("You must registered in a team to complete this operation.")
        team = get_object_or_404(TeamRegistration, teamId=teamId)
        if user != team.captian:
            return HttpResponse('Only captain can remove a player in a team')
        user = get_object_or_404(User, email=form['player'].value())
        user = get_object_or_404(UserProfile, user=user)
        if user.teamId != teamId:
            return HttpResponse("Sorry this player is not in the team")
        user.teamId = None
        user.save()
        return super(removePlayerView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(removePlayerView, self).get_context_data(**kwargs)
        user = get_object_or_404(UserProfile, user=self.request.user)
        users = UserProfile.objects.filter(teamId=user.teamId)
        team = get_object_or_404(TeamRegistration, teamId=user.teamId)
        userList = []
        for i in users:
            userList.append(i)
        userList.remove(team.captian)
        context['players'] = userList
        return context


class TeamViewSet(viewsets.ModelViewSet):
    queryset = TeamRegistration.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
