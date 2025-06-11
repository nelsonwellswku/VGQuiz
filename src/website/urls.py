from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("quiz/<str:slug>/", views.quiz, name="quiz"),
]
