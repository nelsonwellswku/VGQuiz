from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("quiz/:slug", views.quiz, name="quiz"),
]
