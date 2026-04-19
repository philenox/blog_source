from django.shortcuts import render

from .forms import PercentileForm
from .percentile import weight_percentile


def _ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f'{n}{suffix}'


def percentile_view(request):
    form = PercentileForm(request.POST or None)
    result = None
    if request.method == 'POST' and form.is_valid():
        sex = int(form.cleaned_data['sex'])
        age_days = form.cleaned_data['age_days']
        weight_kg = form.cleaned_data['weight_kg']
        calc = weight_percentile(sex, age_days, weight_kg)

        percentile = calc['percentile']
        rounded = int(round(percentile))
        rounded = max(1, min(99, rounded))

        result = {
            'sex_label': 'boy' if sex == 1 else 'girl',
            'age_days': age_days,
            'age_weeks': age_days // 7,
            'age_months_approx': round(age_days / 30.4375, 1),
            'weight_kg': weight_kg,
            'z': calc['z'],
            'percentile': percentile,
            'percentile_rounded': rounded,
            'percentile_ordinal': _ordinal(rounded),
            'median_kg': calc['M'],
        }

    return render(request, 'percentile.html', {
        'form': form,
        'result': result,
    })
