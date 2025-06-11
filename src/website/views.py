from django.http import Http404
from django.shortcuts import render
from database.models import Quiz


def home(request):
    return render(request, "home.html")


def quiz(request, slug):
    try:
        requested_quiz = Quiz.objects.get(slug=slug)
        question = requested_quiz.question_set.order_by("question_id")[0]
        answers = question.answer_set.all()
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist.")

    return render(
        request,
        "quiz.html",
        {
            "data": {
                "video_game_title": requested_quiz.video_game_title,
                "question": question.question_text,
                "answers": answers,
            }
        },
    )
