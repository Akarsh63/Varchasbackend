from django import forms

from registration.models import TeamRegistration
from .models import Match


# forms.TimeField.input_formats = ['%I:%M %p%z'] #['%Y-%m-%dT%H:%M']
class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["event", "match_type", "team1", "team2", "venue", "date", "time", "max_team_size"]
        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
        }

    def clean_team2(self):
        team2 = self.cleaned_data["team2"]
        team1 = self.cleaned_data["team1"]
        if team1 == team2:
            raise forms.ValidationError("BOTH TEAMS CANNOT BE SAME")
        return team2
