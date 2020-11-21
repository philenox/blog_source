from .models import Comment, EmailSubscription
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ('email',)