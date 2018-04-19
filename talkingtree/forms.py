from django.contrib.auth.models import User
from django import forms
from .models import Question, Answer, Comment


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']


class NewQuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea)
    question.widget.attrs.update({'class': 'special'})

    class Meta:
        model = Question
        fields = ['user', 'question_text']


class NewAnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea)
    answer.widget.attrs.update({'class': 'special'})

    class Meta:
        model = Answer
        fields = ['user', 'question', 'answer_text']


class NewCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    comment.widget.attrs.update({'class': 'special'})

    class Meta:
        model = Comment
        fields = ['user', 'answer', 'comment_text']
