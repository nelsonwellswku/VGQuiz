from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from database.models import Quiz
from website.forms import QuizForm


def home(request):
    return render(request, "home.html")


@require_GET
def get_quiz_page(request, slug):
    try:
        requested_quiz = Quiz.objects.get(slug=slug)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist.")

    question = requested_quiz.question_set.order_by("question_id")[0]
    answers = question.answer_set.all()

    return render(
        request,
        "quiz.html",
        {
            "quiz": requested_quiz,
            "question": question,
            "answers": answers,
        },
    )


@require_POST
def post_quiz_answer(request, slug):
    quiz_form = QuizForm(request.POST)

    # todo: what to actually do when the submitted form is invalid?
    if not quiz_form.is_valid():
        raise Http404("Not valid")

    try:
        requested_quiz = Quiz.objects.get(pk=quiz_form.cleaned_data["quiz_id"])
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist.")

    question = requested_quiz.question_set.filter(
        question_id__gt=quiz_form.cleaned_data["question_id"]
    ).order_by("question_id")[0]
    answers = question.answer_set.all()

    return render(
        request,
        "quiz_card.html",
        {"quiz": requested_quiz, "question": question, "answers": answers},
    )

