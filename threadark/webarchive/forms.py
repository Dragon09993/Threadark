from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TwoFactorForm(forms.Form):
    code = forms.UUIDField(label='Verification Code')
    remember_device = forms.BooleanField(required=False, label='Remember this device for 30 days')