from .models import Comment, EmailSubscription
from django import forms
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 10}))
    captcha = CaptchaField()
    class Meta:
        model = Comment
        fields = ('name', 'body')

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ('email',)