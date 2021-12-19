from .models import Comment, EmailSubscription
from django import forms


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 10}))
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ('email',)