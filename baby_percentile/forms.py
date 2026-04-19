from django import forms


SEX_CHOICES = [
    ('1', 'Boy'),
    ('2', 'Girl'),
]


class PercentileForm(forms.Form):
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.RadioSelect)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Baby's date of birth.",
    )
    measurement_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Date the weight was measured.',
    )
    weight_kg = forms.FloatField(
        min_value=0.1,
        max_value=40.0,
        label='Weight (kg)',
        widget=forms.NumberInput(attrs={'step': '0.001'}),
    )

    def clean(self):
        cleaned = super().clean()
        dob = cleaned.get('date_of_birth')
        mdate = cleaned.get('measurement_date')
        if dob and mdate:
            age_days = (mdate - dob).days
            if age_days < 0:
                raise forms.ValidationError(
                    'Measurement date must be on or after date of birth.'
                )
            if age_days > 730:
                raise forms.ValidationError(
                    'This calculator covers ages 0 through 2 years '
                    '(730 days). Your input is older than that.'
                )
            cleaned['age_days'] = age_days
        return cleaned
