from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3, 'cols': 40,
                'placeholder': 'Write your message here...',
                'style': 'resize: none;'
            }),
        }
