from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
