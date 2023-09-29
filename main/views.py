from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
# from .utils import SiteAccessMixin
from .models import NavBarSubOptions, OurTeam, HomeEventCard
from django.shortcuts import get_object_or_404, render
from accounts.models import EsportsUserProfile, UserProfile
from .serializers import OurTeamSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status

class IndexView(TemplateView):

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        if self.request.user.username != "":
            try:
                userprofile = get_object_or_404(UserProfile, user=self.request.user)
            except:
                userprofile = get_object_or_404(EsportsUserProfile, user=self.request.user)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['event_list'] = HomeEventCard.objects.all
        if self.request.user.username != "":
            context['userprofile'] = userprofile
            context['page'] = "home"
        return context

class NavBarSubOptionsPageView(DetailView):
    template_name = 'main/navbarsuboptionpage.html'
    model = NavBarSubOptions

    def get_context_data(self, **kwargs):
        context = super(NavBarSubOptionsPageView, self).get_context_data()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object.use_custom_html:
            self.template_name = self.object.custom_html
        else:
            self.template_name = 'main/navbarsuboptionpage.html'
        return self.render_to_response(context)


class OurTeamView(TemplateView):
    template_name = 'main/our_team.html'
    model = OurTeam

    def get_context_data(self, **kwargs):
        context = super(OurTeamView, self).get_context_data(**kwargs)
        context["our_team"] = OurTeam.objects.all
        context['page'] = "ourTeam"
        if self.request.user.username != "":
            try:
                userprofile = get_object_or_404(UserProfile, user=self.request.user)
            except:
                userprofile = get_object_or_404(EsportsUserProfile, user=self.request.user)
        if self.request.user.username != "":
            context['userprofile'] = userprofile
        return context


def comingSoon(request):
    return render(request, 'main/comingSoon.html')


def error_404(request, exception):
    return render(request, 'main/error_404.html', status=404)


def error_500(request):
    return render(request, 'main/error_500.html', status=500)


class OurTeamViewSet(APIView):
    """
    API endpoint that allows core teams to be viewed, created, updated, or deleted.
    """
    # permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=OurTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_402_PAYMENT_REQUIRED)
        
    def get(self,request):
        teams_data=OurTeam.objects.all()
        if teams_data:
            serializer=OurTeamSerializer(teams_data,many=True)
            if serializer.is_valid:
               return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"No members found"},status=status.HTTP_204_NO_CONTENT)


def gallery(request):
    if request.user.username != "":
        try:
            userprofile = get_object_or_404(UserProfile, user=request.user)
        except:
            userprofile = get_object_or_404(EsportsUserProfile, user=request.user)
    context = {}
    context['user'] = request.user
    if request.user.username != "":
        context['userprofile'] = userprofile
    return render(request, 'main/gallery.html', context)


def payment(request):
    if not request.user.is_authenticated:
        return render(request, "404")
    if request.user.username != "":
        try:
            userprofile = get_object_or_404(UserProfile, user=request.user)
        except:
            userprofile = get_object_or_404(EsportsUserProfile, user=request.user)
            context = {}
            sports = ['All', 'Valorant', 'BGMI', 'Chess']
            context['userprofile'] = userprofile
            context['page'] = "payment"
            if (userprofile.teamId == None):
                context['amount'] = None
            else:
                context['captain'] = userprofile.teamId.captian == userprofile
                context['amount'] = 0
                sport = userprofile.teamId.sport
                context['sports'] = sports[int(sport)]
                if (sport == '1' and userprofile.teamId.captian == userprofile):
                    context['amount'] = 100
                elif (sport == '2' and userprofile.teamId.captian == userprofile):
                    context['amount'] = 100
                elif (sport == '3' and userprofile.teamId.captian == userprofile):
                    context['amount'] = 0
                    userprofile.amount_required = context['amount']
            return render(request, 'main/payment.html', context)
    context = {}
    sports = ['All', 'Athletics', 'Badminton', 'Basketball', 'Chess', 'Cricket', 'Football', 'Table Tennis', 'Tennis',
              'Volleyball', 'Badminton-mixed doubles', 'Squash', 'Kabaddi', 'WeightLifting', 'Table Tennis-Mixed Doubles']
    context['userprofile'] = userprofile
    context['page'] = "payment"
    if (userprofile.teamId == None):
        context['amount'] = None
    else:
        context['captain'] = userprofile.teamId.captian == userprofile
        context['amount'] = 0
        sport = userprofile.teamId.sport
        context['sports'] = sports[int(sport)]
        if (sport == '1' and userprofile.teamId.captian == userprofile):
            if ('4*100m' in userprofile.teamId.subevents or '4*400m' in userprofile.teamId.subevents):
                context['amount'] = 600
            else:
                context['amount'] = 150
        elif (sport == '2' and userprofile.teamId.captian == userprofile and userprofile.gender == 'M'):
            context['amount'] = 1500
        elif (sport == '2' and userprofile.teamId.captian == userprofile and userprofile.gender == 'F'):
            context['amount'] = 1000
        elif (sport == '3' and userprofile.teamId.captian == userprofile and userprofile.gender == 'M'):
            context['amount'] = 2500
        elif (sport == '3' and userprofile.teamId.captian == userprofile and userprofile.gender == 'F'):
            context['amount'] = 1500
        elif (sport == '4' and userprofile.teamId.captian == userprofile):
            context['amount'] = 400
        elif ((sport == '5' or sport == '6') and userprofile.teamId.captian == userprofile):
            context['amount'] = 5000
        elif ((sport == '7') and userprofile.teamId.captian == userprofile and userprofile.gender == 'M'):
            context['amount'] = 1200
        elif ((sport == '7') and userprofile.teamId.captian == userprofile and userprofile.gender == 'F'):
            context['amount'] = 800
        elif (sport == '8' and userprofile.teamId.captian == userprofile):
            context['amount'] = 400
        elif (sport == '9' and userprofile.teamId.captian == userprofile and userprofile.gender == 'M'):
            context['amount'] = 2500
        elif (sport == '9' and userprofile.teamId.captian == userprofile and userprofile.gender == 'F'):
            context['amount'] = 1000
        elif (sport == '10' and userprofile.teamId.captian == userprofile):
            context['amount'] = 600
        elif (sport == '11' and userprofile.teamId.captian == userprofile):
            context['amount'] = 500
        elif (sport == '12' and userprofile.teamId.captian == userprofile):
            context['amount'] = 1500
        elif (sport == '13' and userprofile.teamId.captian == userprofile):
            context['amount'] = 200
        elif (sport == '14' and userprofile.teamId.captian == userprofile):
            context['amount'] = 600

    if (userprofile.accommodation_required == 'Y'):
        context['accommodation'] = 1700
    else:
        context['accommodation'] = 0
    if (context['captain']):
        if (context['amount'] == None):
            userprofile.amount_required = context['accommodation']
        else:
            userprofile.amount_required = context['amount'] + context['accommodation']
    return render(request, 'main/payment.html', context)

def paymentCompletion(request):
    return render(request, 'main/paymentCF.html')


def privacy(request):
    return render(request, 'privacy.html')
