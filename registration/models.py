from django.db import models
from accounts.models import UserProfile,EsportsUserProfile

class TeamRegistration(models.Model):
    SPORT_CHOICES = (
        ('1', 'Athletics'),
        ('2', 'Badminton'),
        ('3', 'Basketball'),
        ('4', 'Cricket'),
        ('5', 'Football'),
        ('6', 'Table Tennis'),
        ('7', 'Lawn Tennis'),
        ('8', 'Volleyball'),
        ('9', 'Kabaddi'),
        ('10', 'Hockey'),
        ('11', 'Squach'),
        ('12', 'Chess'),
        ('13', 'BGMI'),
        ('14','Valorant'),
        ('15', 'Clash Royale'),
    )
    teamId = models.CharField(max_length=15, unique=True, blank=True, null=True)
    sport = models.CharField(max_length=2, choices=SPORT_CHOICES)
    college = models.CharField(max_length=128, blank=True, null=True)
    captian = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    score = models.IntegerField(default=-1)
    category = models.CharField(max_length=1024, blank=True, null=True)
    teams = models.JSONField(blank=True, default=list,null=True)
    teamsize=models.IntegerField(default=1,blank=True,null=True)
    teamcount=models.IntegerField(default=1,blank=True,null=True)
    def __str__(self):
        if (self.teamId == None):
            return "None"
        return self.teamId


class EsportsTeamRegistration(models.Model):
    ESPORT_CHOICES = (
        ('1', 'Valorant'),
        ('2', 'BGMI'),
        ('3', 'Chess')
    )
    teamId = models.CharField(max_length=15, unique=True, blank=True, null=True)
    sport = models.CharField(max_length=2, choices=ESPORT_CHOICES)
    college = models.CharField(max_length=128)
    captian = models.ForeignKey(EsportsUserProfile, on_delete=models.CASCADE, blank=True, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        if (self.teamId == None):
            return "None"
        return self.teamId
