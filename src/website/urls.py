from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("quiz/<int:quiz_id>/<str:slug>/", views.get_quiz_page, name="get_quiz"),
    path("quiz/<int:quiz_id>/answer", views.post_quiz_answer, name="post_quiz_answer"),
]
