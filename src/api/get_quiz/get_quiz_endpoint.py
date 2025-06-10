from ninja import Router, Schema

from database.models import Quiz


router = Router()


class AnswerResponseSchema(Schema):
    answer_id: int
    answer_text: str
    is_correct_answer: bool


class QuestionResponseSchema(Schema):
    question_id: int
    question_text: str
    answers: list[AnswerResponseSchema]


class QuizResponseSchema(Schema):
    quiz_id: int
    video_game_title: str
    questions: list[QuestionResponseSchema]


@router.get("quiz/{int:quiz_id}", response={200: QuizResponseSchema, 404: None})
def get_quiz(request, quiz_id: int):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        return 404, None

    return {
        "quiz_id": quiz_id,
        "video_game_title": quiz.video_game_title,
        "questions": [
            {
                "question_id": q.question_id,
                "question_text": q.question_text,
                "answers": [
                    {
                        "answer_id": answer.answer_id,
                        "answer_text": answer.answer_text,
                        "is_correct_answer": answer.is_correct_answer,
                    }
                    for answer in q.answer_set.all()  # type: ignore
                ],
            }
            for q in quiz.question_set.all()  # type: ignore
        ],
    }
