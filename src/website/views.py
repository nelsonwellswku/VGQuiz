from random import shuffle
import uuid
from django.forms import ValidationError
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Max
from database.models import AnonAnsweredQuestion, Answer, Question, Quiz
from website.forms import QuizForm


def home(request: HttpRequest) -> HttpResponse:
    quizzes = Quiz.objects.order_by("video_game_title").all()[:30]
    return render(request, "home.html", {"quizzes": quizzes})


@require_GET
def get_quiz_page(request: HttpRequest, quiz_id: int, slug: str) -> HttpResponse:
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())

    session_id = request.session["session_id"]

    anon_answered_questions = AnonAnsweredQuestion.objects.filter(
        session_id=session_id, quiz_id=quiz_id
    )
    anon_answered_questions = anon_answered_questions.aggregate(Max("question_id"))
    last_answered_question_id = anon_answered_questions["question_id__max"] or 0

    quiz = Quiz.objects.get(pk=quiz_id)
    total_questions_count = quiz.question_set.count()

    try:
        question = quiz.question_set.filter(
            question_id__gt=last_answered_question_id
        ).order_by("question_id")[0]
    except IndexError:
        anon_answered_questions = (
            AnonAnsweredQuestion.objects.filter(session_id=session_id, quiz_id=quiz_id)
            .select_related("question")
            .select_related("answer")
            .prefetch_related("question__answer_set")
        )

        results = []
        correct_answer_count = 0
        for answered_question in anon_answered_questions:
            all_answers = list(answered_question.question.answer_set.all())
            correct_answer = next(
                filter(lambda answer: answer.is_correct_answer, all_answers)
            )
            answered_correctly = (
                correct_answer.answer_text == answered_question.answer.answer_text
            )
            if answered_correctly:
                correct_answer_count += 1
            results.append(
                {
                    "question": answered_question.question.question_text,
                    "correct_answer": correct_answer.answer_text,
                    "user_answer": answered_question.answer.answer_text,
                    "answered_correctly": answered_correctly,
                }
            )

        return render(
            request,
            "quiz_finished.html",
            {
                "quiz": quiz,
                "results": results,
                "correct_answer_count": correct_answer_count,
                "total_questions_count": total_questions_count,
            },
        )

    questions_remaining = quiz.question_set.filter(
        question_id__gt=last_answered_question_id
    ).count()
    current_question = (total_questions_count - questions_remaining) + 1

    answers = list(question.answer_set.all())
    shuffle(answers)

    return render(
        request,
        "quiz.html",
        {
            "quiz": quiz,
            "question": question,
            "answers": answers,
            "current_question": current_question,
            "total_questions": total_questions_count,
        },
    )


@require_POST
def post_quiz_answer(request: HttpRequest, quiz_id: int) -> HttpResponse:
    quiz_form = QuizForm(request.POST)

    # todo: what to actually do when the submitted form is invalid?
    # maybe just redirect to the quiz page with an error to display in the query string?
    if not quiz_form.is_valid():
        raise ValidationError("Form is invalid")

    session_id = request.session["session_id"]
    quiz_id = quiz_form.cleaned_data["quiz_id"]
    question_id = quiz_form.cleaned_data["question_id"]
    answer_id = quiz_form.cleaned_data["answer_id"]

    try:
        quiz = Quiz.objects.get(pk=quiz_id)
        question = Question.objects.get(pk=question_id)
        answer = Answer.objects.get(pk=answer_id)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist.")
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    except Answer.DoesNotExist:
        raise Http404("Answer does not exist.")

    try:
        anon_answered_question = AnonAnsweredQuestion.objects.filter(
            session_id=session_id,
            quiz_id=quiz_id,
            question_id=question_id,
        )[0]
    except IndexError:
        anon_answered_question = AnonAnsweredQuestion(
            session_id=session_id, quiz=quiz, question=question
        )

    anon_answered_question.answer = answer
    anon_answered_question.save()

    return redirect("get_quiz", quiz.quiz_id, quiz.slug)
