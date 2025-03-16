from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    book_title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Veuillez entrer le titre du livre",
            }
        ),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Veuillez entrer une description",
            }
        ),
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
    )

    class Meta:
        model = Ticket
        fields = ("book_title", "description", "image")


class ReviewForm(forms.ModelForm):
    review_title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Veuillez entrer un titre"}
        ),
    )
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        required=True,
    )
    review = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Veuillez entrer un commentaire",
            }
        ),
    )

    class Meta:
        model = Review
        fields = ["review_title", "rating", "review"]
