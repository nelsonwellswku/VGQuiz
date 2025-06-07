from ninja import NinjaAPI
from app.models import Quiz, Question


api = NinjaAPI()


@api.get("/quiz/{int:quiz_id}")
def get_quiz(request, quiz_id: int):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions: list[Question] = quiz.question_set.all()  # type: ignore
    return {
        "quiz_id": quiz_id,
        "video_game_name": quiz.video_game_name,
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
                ],  # type: ignore
            }
            for q in questions
        ],
    }
