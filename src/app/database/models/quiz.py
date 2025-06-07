from django.db import models

class Quiz(models.Model):
    quiz_id = models.IntegerField(primary_key=True, db_column="QuizId")
    video_game_name = models.CharField("VideoGameName", max_length=255, blank=False, null=False)

class Question(models.Model):
    question_id = models.IntegerField(primary_key=True, db_column="QuestionId")
    question_text = models.CharField(db_column="QuestionText", max_length=255, blank=False, null=False)
    difficulty = models.CharField(db_column="Difficulty", max_length=6, blank=False, null=False)
    question = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING)

class Answer(models.Model):
    answer_id = models.IntegerField(primary_key=True, db_column="AnswerId")
    answer_text = models.CharField(db_column="AnswerText", max_length=255, blank=False, null=False)
    is_correct_answer = models.BooleanField(db_column="IsCorrectAnswer")
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
