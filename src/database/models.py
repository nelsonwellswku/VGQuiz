from django.db import models


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True, db_column="quiz_id")
    video_game_title = models.CharField(
        db_column="video_game_title",
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )

    def __str__(self):
        return self.video_game_title

    class Meta:
        db_table = "Quiz"
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    question_id = models.AutoField(primary_key=True, db_column="question_id")
    question_text = models.CharField(
        db_column="question_text", max_length=255, blank=False, null=False
    )
    difficulty = models.CharField(
        db_column="difficulty", max_length=6, blank=False, null=False
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING, db_column="quiz_id")

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = "Question"


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True, db_column="answer_id")
    answer_text = models.CharField(
        db_column="answer_text", max_length=255, blank=False, null=False
    )
    is_correct_answer = models.BooleanField(db_column="is_correct_answer")
    question = models.ForeignKey(
        Question, db_column="question_id", on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.answer_text

    class Meta:
        db_table = "Answer"
