from django.db import models
from accounts.models import EsportsUserProfile, UserProfile


class TeamRegistration(models.Model):
    SPORT_CHOICES = (
        ('1', 'Athletics'),
        ('2', 'Badminton'),
        ('3', 'Basketball'),
        ('4', 'Chess'),
        ('5', 'Cricket'),
        ('6', 'Football'),
        ('7', 'Table Tennis'),
        ('8', 'Tennis'),
        ('9', 'Volleyball'),
        # ('10', 'Badminton-Mixed doubles'),
        # ('11', 'Squash'),
        ('10', 'Kabaddi'),
        # ('13', 'WeightLifting'),
        ('11', 'Table Tennis-Mixed doubles'),
    )
    teamId = models.CharField(max_length=15, unique=True, blank=True, null=True)
    sport = models.CharField(max_length=2, choices=SPORT_CHOICES)
    college = models.CharField(max_length=128)
    captian = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    score = models.IntegerField(default=0)
    subevents = models.CharField(max_length=1024, blank=True, null=True)

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
