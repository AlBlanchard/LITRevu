from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Veuillez entrer un titre"}
        ),
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Veuillez entrer une description",
            }
        ),
    )
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
    )

    class Meta:
        model = Ticket
        fields = ("title", "description", "image")
