from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from database.models import Quiz
from website.forms import QuizForm


def home(request):
    quizzes = Quiz.objects.all()[:10]
    return render(request, "home.html", {"quizzes": quizzes})


@require_GET
def get_quiz_page(request, slug):
    try:
        requested_quiz = Quiz.objects.get(slug=slug)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist.")

    total_questions = requested_quiz.question_set.count()
    question = requested_quiz.question_set.order_by("question_id")[0]
    answers = question.answer_set.all()

    return render(
        request,
        "quiz.html",
        {
            "quiz": requested_quiz,
            "question": question,
            "answers": answers,
            "current_question": 1,
            "total_questions": total_questions,
        },
    )


@require_POST
def post_quiz_answer(request, slug):
    quiz_form = QuizForm(request.POST)

    # todo: what to actually do when the submitted form is invalid?
    if not quiz_form.is_valid():
        raise ValidationError("Form is invalid")

    quiz_id = quiz_form.cleaned_data["quiz_id"]
    question_id = quiz_form.cleaned_data["question_id"]

    try:
        requested_quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist.")

    try:
        question = requested_quiz.question_set.filter(
            question_id__gt=question_id
        ).order_by("question_id")[0]
    except IndexError:
        return render(request, "quiz_card_finished.html")

    total_questions = requested_quiz.question_set.count()
    questions_remaining = (
        requested_quiz.question_set.filter(question_id__gt=question_id).count() + 1
    )
    current_question = total_questions - questions_remaining
    answers = question.answer_set.all()

    return render(
        request,
        "quiz_card.html",
        {
            "quiz": requested_quiz,
            "question": question,
            "answers": answers,
            "current_question": current_question,
            "total_questions": total_questions,
        },
    )
