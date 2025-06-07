from django.contrib import admin
from app.models import Quiz, Question, Answer

class QuizAdmin(admin.ModelAdmin):
    readonly_fields = ["quiz_id"]

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ["question_id"]

class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ["answer_id"]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
