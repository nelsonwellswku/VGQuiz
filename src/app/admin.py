from django.contrib import admin
from app.models import Quiz, Question, Answer

class QuizAdmin(admin.ModelAdmin):
    fields = ["quiz_id", "video_game_name"]
    readonly_fields = ["quiz_id"]

class QuestionAdmin(admin.ModelAdmin):
    fields = ["question_id", "quiz", "difficulty", "question_text"]
    readonly_fields = ["question_id"]

class AnswerAdmin(admin.ModelAdmin):
    fields = ["answer_id", "question", "answer_text", "is_correct_answer"]
    readonly_fields = ["answer_id"]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
