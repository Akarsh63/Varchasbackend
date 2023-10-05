from django.views.generic import TemplateView
from .models import OurTeam
from django.shortcuts import get_object_or_404, render
from accounts.models import  UserProfile
from .serializers import OurTeamSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status

class IndexView(TemplateView):

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.username != "":
            context['page'] = "home"
        return context

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
        
    def get(self, request):
        teams_data = OurTeam.objects.all()
        if not teams_data:
            return Response({"message": "No members found"}, status=status.HTTP_204_NO_CONTENT)
        grouped_data = {}
        for team_member in teams_data:
            position_id = team_member.position
            if position_id not in grouped_data:
                grouped_data[position_id] = []
            serialized_member = OurTeamSerializer(team_member).data
            grouped_data[position_id].append(serialized_member)
        return Response(grouped_data, status=status.HTTP_200_OK)

def error_404(request, exception):
    return render(request, 'main/error_404.html', status=404)

def error_500(request):
    return render(request, 'main/error_500.html', status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment(request):
    user_id = request.user
    try:
        userprofile = get_object_or_404(UserProfile, user=user_id)
    except UserProfile.DoesNotExist:
        return Response({"message": "User not registered yet!"}, status=status.HTTP_404_NOT_FOUND)

    if userprofile.teamId is None:
        return Response({"message": "You have to first register in a team."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        sport = userprofile.teamId.sport
        if userprofile.teamId.captian != userprofile:
           return Response({"message":'Ask your captain to complete the payment. If already done, please ignore.'})
        amount=0
        if sport == '2' and userprofile.teamId.captian == userprofile :
           if userprofile.teamId.category=='men':
               amount=1500
           elif userprofile.teamId.category=='women':
               amount=1200
           else:
               amount =1000
        elif sport == '3' and userprofile.teamId.captian == userprofile :
            if userprofile.teamId.category=='men':
               amount=3500
            elif userprofile.teamId.category=='women':
               amount=2500
        elif sport == '4' and userprofile.teamId.captian == userprofile :
            if userprofile.teamId.category=='men':
               amount=5000
        elif sport == '5' and userprofile.teamId.captian == userprofile :
            if userprofile.teamId.category=='men':
               amount=5000
            elif userprofile.teamId.category=='women':
               amount=3000
        elif sport == '6' and userprofile.teamId.captian == userprofile :
            if userprofile.teamId.category=='men':
               amount=1500
            elif userprofile.teamId.category=='women':
               amount=1200
        elif sport == '7' and userprofile.teamId.captian == userprofile :
            if userprofile.teamId.category=='men':
               amount=1200
        elif sport == '8' and userprofile.teamId.captian == userprofile :
            if userprofile.teamId.category=='men':
               amount=3500
            elif userprofile.teamId.category=='women':
               amount=2500
        elif sport == '9' and userprofile.teamId.captian == userprofile :
            if userprofile.teamId.category=='men':
               amount=3500
        elif sport == '10' and userprofile.teamId.captian == userprofile :
            if userprofile.teamId.category=='men':
               amount=3500
        elif sport == '11' and userprofile.teamId.captian == userprofile :
            amount=500
        elif sport == '12' and userprofile.teamId.captian == userprofile :
            amount=200
        #   not comp
        elif sport == '13' and userprofile.teamId.captian == userprofile :
            amount=99
        elif sport == '14' and userprofile.teamId.captian == userprofile :
            amount=499
        elif sport == '15' and userprofile.teamId.captian == userprofile :
            amount=99
        
        userprofile.amount_required=amount
        userprofile.save()

        return Response({"amount":amount})
  
        