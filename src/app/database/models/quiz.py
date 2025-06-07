from django.db import models


class Quiz(models.Model):
    quiz_id = models.IntegerField(primary_key=True, db_column="QuizId")
    video_game_name = models.CharField(
        db_column="VideoGameName", max_length=255, blank=False, null=False
    )

    def __str__(self):
        return self.video_game_name

    class Meta:
        db_table = "Quiz"


class Question(models.Model):
    question_id = models.IntegerField(primary_key=True, db_column="QuestionId")
    question_text = models.CharField(
        db_column="QuestionText", max_length=255, blank=False, null=False
    )
    difficulty = models.CharField(
        db_column="Difficulty", max_length=6, blank=False, null=False
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING, db_column="QuizId")

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = "Question"


class Answer(models.Model):
    answer_id = models.IntegerField(primary_key=True, db_column="AnswerId")
    answer_text = models.CharField(
        db_column="AnswerText", max_length=255, blank=False, null=False
    )
    is_correct_answer = models.BooleanField(db_column="IsCorrectAnswer")
    question = models.ForeignKey(
        Question, db_column="QuestionId", on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.answer_text

    class Meta:
        db_table = "Answer"
