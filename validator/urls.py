from django.urls import path

from . import views

app_name = 'validator'

urlpatterns = [
    path("", views.index, name="index"),
    path('validate/', views.validate_credit_card, name='validate_credit_card'),
]