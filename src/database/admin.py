from django.contrib import admin
from .models import Platform, Quiz, Question, Answer


class AnswerInline(admin.TabularInline):
    fields = ["answer_id", "question", "answer_text", "is_correct_answer"]
    readonly_fields = ["answer_id"]
    model = Answer
    max_num = 4
    min_num = 4
    can_delete = False


class PlatformAdmin(admin.ModelAdmin):
    fields = ["short_name", "long_name"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "quiz", "difficulty"]
    fields = ["question_id", "quiz", "question_text", "difficulty"]
    readonly_fields = ["question_id", "quiz"]
    inlines = [AnswerInline]


class QuestionInline(admin.TabularInline):
    readonly_fields = ["question_text", "difficulty"]
    model = Question
    show_change_link = True
    can_delete = False


class QuizAdmin(admin.ModelAdmin):
    list_display = ["video_game_title", "platform"]
    readonly_fields = ["quiz_id", "slug", "platform"]
    inlines = [QuestionInline]


admin.site.register(Platform, PlatformAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
