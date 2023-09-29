from django.views.generic import FormView

from registration.models import TeamRegistration
from .forms import MatchForm
from .models import Match, Event, Cricket, Volleyball, Football, BasketBall, Chess, Squash, Badminton, TT, Tennis
from django.contrib import messages
from rest_framework import viewsets
from .serializers import BasketballSerializer, CricketSerializer, FootballSerializer, VolleyballSerializer, ChessSerializer, SquashSerializer, BadmintonSerializer, TTSerializer, TennisSerializer, MatchSerializer
from rest_framework import permissions
from django.shortcuts import render


class CreateMatch(FormView):
    template_name = 'events/add_match.html'
    form_class = MatchForm
    success_url = '/events/add'

    def form_valid(self, form):
        data = self.request.POST.copy()
        game_ch = Event.EVENT_CHOICES[int(data['event']) - 1][1][:2].upper()
        type_ch = Match.MATCH_CHOICES[int(data['match_type']) - 1][1][:2].upper()
        data['event_id'] = game_ch + '-' + type_ch + '-' + data['team1'][:2].upper() + data['team2'][:2].upper()
        form = MatchForm(data)
        if Match.objects.filter(event_id=data['event_id']).exists():
            message = "You are already in team {}".format(data['event_id'])
        else:
            message = "Match created with Match ID {}".format(data['event_id'])
            obj = form.save()
            obj.event_id = data['event_id']
            obj.save()
            CreateMatch.create_match(obj, **form.cleaned_data)
        messages.success(self.request, message)
        return super(CreateMatch, self).form_valid(form)

    @staticmethod
    def create_match(match=None, **kwargs):
        if kwargs['event'] == '9':
            sport = Volleyball(match=match)
        elif kwargs['event'] == '6':
            sport = Football(match=match)
        elif kwargs['event'] == '5':
            sport = Cricket(match=match)
        elif kwargs['event'] == '3':
            sport = BasketBall(match=match)
        elif kwargs['event'] == '7':
            sport = TT(match=match)
        elif kwargs['event'] == '2':
            sport = Badminton(match=match)
        elif kwargs['event'] == '8':
            sport = Tennis(match=match)
        sport.save()

    def get_template_names(self):
        if not self.request.user.is_superuser:
            return "main/error_404.html"
        return super().get_template_names()


class CricketViewSet(viewsets.ModelViewSet):
    queryset = Cricket.objects.all()
    serializer_class = CricketSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FootballViewSet(viewsets.ModelViewSet):
    queryset = Football.objects.all()
    serializer_class = FootballSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class VolleyballViewSet(viewsets.ModelViewSet):
    queryset = Volleyball.objects.all()
    serializer_class = VolleyballSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ChessViewSet(viewsets.ModelViewSet):
    queryset = Chess.objects.all()
    serializer_class = ChessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SquashViewSet(viewsets.ModelViewSet):
    queryset = Squash.objects.all()
    serializer_class = SquashSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BadmintonViewSet(viewsets.ModelViewSet):
    queryset = Badminton.objects.all()
    serializer_class = BadmintonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BasketballViewSet(viewsets.ModelViewSet):
    queryset = BasketBall.objects.all()
    serializer_class = BasketballSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TTViewSet(viewsets.ModelViewSet):
    queryset = TT.objects.all()
    serializer_class = TTSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TennisViewSet(viewsets.ModelViewSet):
    queryset = Tennis.objects.all()
    serializer_class = TennisSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


def cricket(request):
    context = {}
    context['fixtures'] = Cricket.objects.all().order_by('-match__event__date')
    context['leaderboard'] = TeamRegistration.objects.all().filter(sport='5').order_by('-score')
    return render(request, 'events/cricket.html', context)


def football(request):
    context = {}
    context['fixtures'] = Football.objects.all()
    context['leaderboard'] = TeamRegistration.objects.all().filter(sport='6').order_by('-score')
    return render(request, 'events/football.html', context)


def volleyball(request):
    context = {}
    context['fixtures'] = Volleyball.objects.all()
    context['leaderboard'] = TeamRegistration.objects.all().filter(sport='9').order_by('-score')
    return render(request, 'events/volleyball.html', context)


def chess(request):
    context = {}
    context['fixtures'] = Chess.objects.all()
    context['leaderboard'] = TeamRegistration.objects.all().filter(sport='4').order_by('-score')
    return render(request, 'events/chess.html', context)


def squash(request):
    return render(request, 'events/squash.html')


def TT(request):
    context = {}
    return render(request, 'events/TT.html', context)


def badminton(request):
    context = {}
    context['fixtures'] = Badminton.objects.all()
    context['leaderboard'] = TeamRegistration.objects.all().filter(sport='2').order_by('-score')
    return render(request, 'events/badminton.html', context)


def tennis(request):
    context = {}
    context['fixtures'] = Tennis.objects.all()
    context['leaderboard'] = TeamRegistration.objects.all().filter(sport='8').order_by('-score')
    return render(request, 'events/tennis.html', context)


def athletics(request):
    return render(request, 'events/athletics.html')


def kabaddi(request):
    return render(request, 'events/kabaddi.html')


def weightlifting(request):
    return render(request, 'events/weightlifting.html')


def informals(request):
    return render(request, 'events/informals.html')


def basketball(request):
    context = {}
    context['fixtures'] = BasketBall.objects.all()
    context['leaderboard'] = TeamRegistration.objects.all().filter(sport='3').order_by('-score')
    return render(request, 'events/basketball.html', context)


def valorant(request):
    return render(request, 'events/valorant.html')


def bgmi(request):
    return render(request, 'events/bgmi.html')


def fixtures(request, sport):
    # sport = request.POST.get('sport')
    context = {}
    if (sport == '5'):
        teams = []
        context['fixtures'] = Cricket.objects.all()
        # print(context['fixtures'])
        context['sport'] = "Cricket"
        for i in context['fixtures']:
            if (i.match == None):
                i.delete()
                continue
            teams.append(i.match.team1)
            teams.append(i.match.team2)
        teams = list(set(teams))
        teams = sorted(teams, key=lambda p: p.score)[::-1]
        context['leaderboard'] = teams
    if (sport == '2'):
        teams = []
        context['fixtures'] = Badminton.objects.all().exclude(match=None).order_by('-match__date')
        print(context['fixtures'])
        context['sport'] = "Badminton"
        for i in context['fixtures']:
            teams.append(i.match.team1)
            teams.append(i.match.team2)
        teams = list(set(teams))
        teams = sorted(teams, key=lambda p: p.score)[::-1]
        context['leaderboard'] = teams
    if (sport == '3'):
        teams = []
        context['fixtures'] = BasketBall.objects.all().exclude(match=None).order_by('-match__date')
        print(context['fixtures'])
        context['sport'] = "Basketball"
        for i in context['fixtures']:
            teams.append(i.match.team1)
            teams.append(i.match.team2)
        teams = list(set(teams))
        teams = sorted(teams, key=lambda p: p.score)[::-1]
        context['leaderboard'] = teams
    if (sport == '6'):
        teams = []
        context['fixtures'] = Football.objects.all().exclude(match=None).order_by('-match__date')
        print(context['fixtures'])
        context['sport'] = "Football"
        for i in context['fixtures']:
            teams.append(i.match.team1)
            teams.append(i.match.team2)
        teams = list(set(teams))
        teams = sorted(teams, key=lambda p: p.score)[::-1]
        context['leaderboard'] = teams
    if (sport == '7'):
        teams = []
        context['fixtures'] = TT.objects.all().exclude(match=None).order_by('-match__date')
        print(context['fixtures'])
        context['sport'] = "Table Tennis"
        for i in context['fixtures']:
            teams.append(i.match.team1)
            teams.append(i.match.team2)
        teams = list(set(teams))
        teams = sorted(teams, key=lambda p: p.score)[::-1]
        context['leaderboard'] = teams
    if (sport == '8'):
        teams = []
        context['fixtures'] = Tennis.objects.all().exclude(match=None).order_by('-match__date')
        print(context['fixtures'])
        context['sport'] = "Tennis"
        for i in context['fixtures']:
            teams.append(i.match.team1)
            teams.append(i.match.team2)
        teams = list(set(teams))
        teams = sorted(teams, key=lambda p: p.score)[::-1]
        context['leaderboard'] = teams
    if (sport == '9'):
        teams = []
        context['fixtures'] = Volleyball.objects.all().exclude(match=None).order_by('-match__date')
        print(context['fixtures'])
        context['sport'] = "Volleyball"
        for i in context['fixtures']:
            teams.append(i.match.team1)
            teams.append(i.match.team2)
        teams = list(set(teams))
        teams = sorted(teams, key=lambda p: p.score)[::-1]
        context['leaderboard'] = teams
    return render(request, 'events/fixtures.html', context)
