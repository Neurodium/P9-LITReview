from django import forms
from .models import Ticket, Review
from django.utils.safestring import mark_safe

class SubscribeForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


REVIEW_RATINGS =(
    ("0", "- 0"),
    ("1", "- 1"),
    ("2", "- 2"),
    ("3", "- 3"),
    ("4", "- 4"),
    ("5", "- 5"),
)

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=REVIEW_RATINGS, widget=forms.RadioSelect)
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
