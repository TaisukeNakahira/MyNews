# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'sample2'

urlpatterns = [
    path('', views.test, name = 'sample2'),
]