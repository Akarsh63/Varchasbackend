from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import UserProfile, EsportsUserProfile


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'maxlength': '254', 'placeholder': ' ', 'autocomplete': 'off'}))
    password1 = forms.CharField(
        min_length=8,
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    phone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'placeholder': ' '}))
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True,
                               widget=forms.Select(attrs={'class': 'mdb-select'}))
    college = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    state = forms.ChoiceField(choices=UserProfile.STATE_CHOICES, required=True,
                              widget=forms.Select(attrs={'class': 'mdb-select'}))

    accommodation_required = forms.ChoiceField(choices=UserProfile.ACCOMMODATION_CHOICES,
                                               widget=forms.Select(attrs={'class': 'mdb-select'}), required=False)
    referred_by = forms.CharField(
        max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': ' '}))
    undertaking_signed = forms.BooleanField(label="Undertaking Signed", widget=forms.CheckboxInput, required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'username']

    def clean_first_name(self):
        _dict = super(RegisterForm, self).clean()
        return _dict['first_name'].capitalize()

    def clean_phone(self):
        _dict = super(RegisterForm, self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']

    def clean_last_name(self):
        _dict = super(RegisterForm, self).clean()
        return _dict['last_name'].capitalize()

    def clean_email(self):
        if User.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['icon_name'] = "fa fa-envelope"
        self.fields['username'].widget.attrs['icon_name'] = "fa fa-id-card"
        self.fields['first_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['last_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['password1'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['password2'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['phone'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"


class EsportsRegisterFormValorant(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' ', 'icon': 'a'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'maxlength': '254', 'placeholder': ' ', 'autocomplete': 'off'}))

    password1 = forms.CharField(
        min_length=8,
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    phone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'placeholder': ' '}))
    gender = forms.ChoiceField(choices=EsportsUserProfile.GENDER_CHOICES, required=True,
                               widget=forms.Select(attrs={'class': 'mdb-select'}))
    college = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    state = forms.ChoiceField(choices=EsportsUserProfile.STATE_CHOICES, required=True,
                              widget=forms.Select(attrs={'class': 'mdb-select'}))
    captain_ingame_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    captain_peak_rank = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_2_Name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_2_ingame_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_2_peak_rank = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_3_Name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_3_ingame_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_3_peak_rank = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_4_Name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_4_ingame_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_4_peak_rank = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_5_Name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_5_ingame_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_5_peak_rank = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_6_Name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=False)
    Member_6_ingame_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=False)
    Member_6_peak_rank = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=False)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'username']

    def clean_first_name(self):
        _dict = super(EsportsRegisterFormValorant, self).clean()
        return _dict['first_name'].capitalize()

    def clean_phone(self):
        _dict = super(EsportsRegisterFormValorant, self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']

    def clean_last_name(self):
        _dict = super(EsportsRegisterFormValorant, self).clean()
        return _dict['last_name'].capitalize()

    def clean_email(self):
        if User.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']

    def __init__(self, *args, **kwargs):
        super(EsportsRegisterFormValorant, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['icon_name'] = "fa fa-envelope"
        self.fields['username'].widget.attrs['icon_name'] = "fa fa-id-card"
        self.fields['first_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['last_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['password1'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['password2'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['phone'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"


class EsportsRegisterFormBGMI(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' ', 'icon': 'a'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'maxlength': '254', 'placeholder': ' ', 'autocomplete': 'off'}))

    password1 = forms.CharField(
        min_length=8,
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    phone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'placeholder': ' '}))
    gender = forms.ChoiceField(choices=EsportsUserProfile.GENDER_CHOICES, required=True,
                               widget=forms.Select(attrs={'class': 'mdb-select'}))
    college = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    state = forms.ChoiceField(choices=EsportsUserProfile.STATE_CHOICES, required=True,
                              widget=forms.Select(attrs={'class': 'mdb-select'}))
    captain_character_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    captain_ingame_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_2_Name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_2_ingame_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_2_character_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_3_Name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_3_ingame_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_3_character_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_4_Name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_4_ingame_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    Member_4_character_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'username']

    def clean_first_name(self):
        _dict = super(EsportsRegisterFormBGMI, self).clean()
        return _dict['first_name'].capitalize()

    def clean_phone(self):
        _dict = super(EsportsRegisterFormBGMI, self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']

    def clean_last_name(self):
        _dict = super(EsportsRegisterFormBGMI, self).clean()
        return _dict['last_name'].capitalize()

    def clean_email(self):
        if User.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']

    def __init__(self, *args, **kwargs):
        super(EsportsRegisterFormBGMI, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['icon_name'] = "fa fa-envelope"
        self.fields['username'].widget.attrs['icon_name'] = "fa fa-id-card"
        self.fields['first_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['last_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['password1'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['password2'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['phone'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"


class EsportsRegisterFormChess(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' ', 'icon': 'a'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'maxlength': '254', 'placeholder': ' ', 'autocomplete': 'off'}))

    password1 = forms.CharField(
        min_length=8,
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    phone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'placeholder': ' '}))
    gender = forms.ChoiceField(choices=EsportsUserProfile.GENDER_CHOICES, required=True,
                               widget=forms.Select(attrs={'class': 'mdb-select'}))
    college = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    state = forms.ChoiceField(choices=EsportsUserProfile.STATE_CHOICES, required=True,
                              widget=forms.Select(attrs={'class': 'mdb-select'}))
    Lichess_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=False)
    Chesscom_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=False)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'username']

    def clean_first_name(self):
        _dict = super(EsportsRegisterFormChess, self).clean()
        return _dict['first_name'].capitalize()

    def clean_phone(self):
        _dict = super(EsportsRegisterFormChess, self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']

    def clean_last_name(self):
        _dict = super(EsportsRegisterFormChess, self).clean()
        return _dict['last_name'].capitalize()

    def clean_email(self):
        if User.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']

    def __init__(self, *args, **kwargs):
        super(EsportsRegisterFormChess, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['icon_name'] = "fa fa-envelope"
        self.fields['username'].widget.attrs['icon_name'] = "fa fa-id-card"
        self.fields['first_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['last_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['password1'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['password2'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['phone'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"


class PasswordResetCaptchaForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': ' ', 'type': 'email', 'maxlength': '254'}))
