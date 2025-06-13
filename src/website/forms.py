from django import forms


class QuizForm(forms.Form):
    quiz_id = forms.IntegerField()
    question_id = forms.IntegerField()
    answer_id = forms.IntegerField()
