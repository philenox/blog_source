from .models import Comment, EmailSubscription
from django import forms
from django.core import signing
from django_recaptcha.fields import ReCaptchaField
import time


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 10}))
    captcha = ReCaptchaField()
    # Honeypot: hidden via CSS; bots fill it, humans don't see it
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'tabindex': '-1',
            'autocomplete': 'off',
            'aria-hidden': 'true',
            'class': 'hp-field',
        })
    )
    # Signed timestamp set on page load; validates minimum elapsed time
    form_load_time = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ('name', 'body')

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError("Bot detected.")
        return ''

    def clean_form_load_time(self):
        value = self.cleaned_data.get('form_load_time', '')
        try:
            load_time = signing.loads(value, max_age=86400)
            if time.time() - load_time < 5:
                raise forms.ValidationError(
                    "Your comment was submitted too quickly. Please try again."
                )
        except signing.SignatureExpired:
            raise forms.ValidationError(
                "Form session expired. Please reload the page and try again."
            )
        except Exception:
            raise forms.ValidationError("Invalid form submission.")
        return value

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ('email',)