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


@router.post("quiz", response=CreateQuizResponse)
def create_quiz(request, body: CreateQuizRequest):
    try:
        with transaction.atomic():
            try:
                platform = Platform.objects.get(short_name=body.platform)
            except Platform.DoesNotExist:
                platform = Platform(short_name=body.platform)
                platform.save()

            new_quiz = Quiz(video_game_title=body.video_game_title, platform=platform)
            new_quiz.save()

            for question in body.questions:
                new_question = Question(
                    difficulty=question.difficulty, question_text=question.question_text
                )
                new_question.quiz = new_quiz
                new_question.save()
                for answer in question.answers:
                    new_answer = Answer(
                        answer_text=answer.answer_text,
                        is_correct_answer=answer.is_correct_answer,
                    )
                    new_answer.question = new_question
                    new_answer.save()
    except Exception as e:
        print("Unable to commit transaction.", e)
        raise

    return {"quiz_id": new_quiz.quiz_id}
