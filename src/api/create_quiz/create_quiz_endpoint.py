from django.db import transaction
from ninja import Schema, Router

from database.models import Answer, Platform, Question, Quiz

router = Router()


class AnswerRequestSchema(Schema):
    answer_text: str
    is_correct_answer: bool


class QuestionRequestSchema(Schema):
    question_text: str
    difficulty: str
    answers: list[AnswerRequestSchema]


class CreateQuizRequest(Schema):
    video_game_title: str
    platform: str
    questions: list[QuestionRequestSchema]


class CreateQuizResponse(Schema):
    quiz_id: int


class QuizAlreadyExistsResponse(Schema):
    quiz_id: int
    message: str


@router.post("quiz", response={200: CreateQuizResponse, 409: QuizAlreadyExistsResponse})
def create_quiz(request, body: CreateQuizRequest):
    try:
        with transaction.atomic():
            try:
                platform = Platform.objects.get(short_name=body.platform)
            except Platform.DoesNotExist:
                platform = Platform(short_name=body.platform)
                platform.save()

            quiz = None
            try:
                quiz = Quiz.objects.get(video_game_title=body.video_game_title)
            except Quiz.DoesNotExist:
                pass

            if quiz:
                return 409, {"quiz_id": quiz.quiz_id, "message": "Quiz already exists."}

            quiz = Quiz(video_game_title=body.video_game_title, platform=platform)
            quiz.save()

            for body_question in body.questions:
                question = Question(
                    difficulty=body_question.difficulty,
                    question_text=body_question.question_text,
                )
                question.quiz = quiz
                question.save()
                for body_answer in body_question.answers:
                    answer = Answer(
                        answer_text=body_answer.answer_text,
                        is_correct_answer=body_answer.is_correct_answer,
                    )
                    answer.question = question
                    answer.save()
    except Exception as e:
        print("Unable to commit transaction.", e)
        raise

    return {"quiz_id": quiz.quiz_id}
