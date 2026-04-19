from django.urls import path

from . import views

urlpatterns = [
    path('', views.percentile_view, name='baby_percentile'),
]
