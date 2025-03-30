from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    book_title = forms.CharField(
        label="Titre",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    description = forms.CharField(
        max_length=800,
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
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
        label="Titre",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        required=True,
    )
    review = forms.CharField(
        label="Commentaire",
        max_length=800,
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Review
        fields = ["review_title", "rating", "review"]
