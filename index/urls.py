from django.contrib import admin
from django.urls import path
from . import views

app_name = "index"

urlpatterns = [
    path('create/',views.index, name = "index"),
    #path('home/',views.index, name = "index"),

]