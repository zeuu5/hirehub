# forms.py
from django import forms
from .models import Services,Review

class ServiceSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255, required=False)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['title', 'description', 'price', 'image', 'latitude', 'longitude']

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Write your review...', 'rows': 3}),
        }
