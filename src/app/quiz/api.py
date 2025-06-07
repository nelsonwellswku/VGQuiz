from ninja import Router, Schema
from app.models import Quiz

router = Router()

class AnswerResponseSchema(Schema):
    answerId: int
    answerText: str
    isCorrectAnswer: bool

class QuestionResponseSchema(Schema):
    questionId: int
    questionText: str
    answers: list[AnswerResponseSchema]

class QuizResponseSchema(Schema):
    quizId: int
    videoGameName: str
    questions: list[QuestionResponseSchema]

@router.get("quiz/{int:quiz_id}", response=QuizResponseSchema)
def get_quiz(request, quiz_id: int):
    quiz = Quiz.objects.get(pk=quiz_id)
    return {
        "quizId": quiz_id,
        "videoGameName": quiz.video_game_name,
        "questions": [
            {
                "questionId": q.question_id,
                "questionText": q.question_text,
                "answers": [
                    {
                        "answerId": answer.answer_id,
                        "answerText": answer.answer_text,
                        "isCorrectAnswer": answer.is_correct_answer,
                    }
                    for answer in q.answer_set.all()  # type: ignore
                ],
            }
            for q in quiz.question_set.all()  # type: ignore
        ],
    }
