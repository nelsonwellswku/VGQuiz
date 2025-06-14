from django.contrib import admin
from .models import Quiz, Question, Answer


class AnswerInline(admin.TabularInline):
    fields = ["answer_id", "question", "answer_text", "is_correct_answer"]
    readonly_fields = ["answer_id"]
    model = Answer
    max_num = 4
    min_num = 4
    can_delete = False


class QuestionAdmin(admin.ModelAdmin):
    fields = ["question_id", "quiz", "difficulty", "question_text"]
    readonly_fields = ["question_id"]
    inlines = [AnswerInline]


class QuestionInline(admin.TabularInline):
    fields = ["question_id", "quiz", "question_text", "difficulty"]
    readonly_fields = ["question_id"]
    model = Question
    show_change_link = True
    can_delete = False


class QuizAdmin(admin.ModelAdmin):
    fields = ["quiz_id", "video_game_title", "slug"]
    readonly_fields = ["quiz_id", "slug"]
    inlines = [QuestionInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
