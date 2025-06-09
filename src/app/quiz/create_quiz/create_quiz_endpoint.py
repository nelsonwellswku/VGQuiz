from django.db import transaction
from ninja import Schema, Router

from app.database.models.quiz import Answer, Question, Quiz

router = Router()


class AnswerRequestSchema(Schema):
    answerText: str
    isCorrectAnswer: bool


class QuestionRequestSchema(Schema):
    questionText: str
    difficulty: str
    answers: list[AnswerRequestSchema]


class CreateQuizRequest(Schema):
    videoGameName: str
    questions: list[QuestionRequestSchema]


class CreateQuizResponse(Schema):
    quizId: int


@router.post("quiz", response=CreateQuizResponse)
def create_quiz(request, body: CreateQuizRequest):
    try:
        with transaction.atomic():
            new_quiz = Quiz()
            new_quiz.video_game_name = body.videoGameName
            new_quiz.save()

            for question in body.questions:
                new_question = Question()
                new_question.difficulty = question.difficulty
                new_question.question_text = question.questionText
                new_question.quiz = new_quiz
                new_question.save()
                for answer in question.answers:
                    new_answer = Answer()
                    new_answer.answer_text = answer.answerText
                    new_answer.is_correct_answer = answer.isCorrectAnswer
                    new_answer.question = new_question
                    new_answer.save()
    except Exception as e:
        print("Unable to commit transaction.", e)
        raise

    return {"quizId": new_quiz.quiz_id}
