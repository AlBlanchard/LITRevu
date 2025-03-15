from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}
        ),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Mot de passe"}
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirmer le mot de passe"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Les mots de passe ne correspondent pas. Veuillez réessayer."
            )

        return password2


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}
        ),
        required=True,
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Mot de passe"}
        ),
        required=True,
    )
