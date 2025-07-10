from django.db import models
from django.utils.text import slugify


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True, db_column="platform_id")
    short_name = models.CharField(max_length=32, blank=False, null=False)
    long_name = models.CharField(max_length=128, blank=False, null=True)

    def __str__(self):
        return self.short_name

    class Meta:
        db_table = "Platform"


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True, db_column="quiz_id")
    video_game_title = models.CharField(
        db_column="video_game_title",
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(db_column="slug", max_length=255, unique=True)
    box_art = models.ImageField(
        upload_to="box_art", db_column="box_art", blank=False, null=True
    )
    platform = models.ForeignKey(
        Platform, on_delete=models.CASCADE, db_column="platform_id"
    )

    question_set: models.QuerySet["Question"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.video_game_title}-{self.platform.short_name}")
        super(Quiz, self).save(*args, **kwargs)

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
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column="quiz_id")
    answer_set: models.QuerySet["Answer"]

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
        Question, db_column="question_id", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.answer_text

    class Meta:
        db_table = "Answer"


class AnonAnsweredQuestion(models.Model):
    user_answered_question_id = models.AutoField(
        primary_key=True, db_column="user_answered_question_id"
    )
    session_id = models.UUIDField(db_column="session_id")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column="quiz_id")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, db_column="question_id"
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, db_column="answer_id")

    class Meta:
        db_table = "AnonAnsweredQuestion"
