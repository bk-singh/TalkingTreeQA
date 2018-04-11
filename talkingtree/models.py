from django.db import models
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import datetime
from django.contrib.auth.models import User


class Question(models.Model):
    # user_id = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: rename question_text to text
    question_text = models.CharField(max_length=200)
    created_date = models.DateTimeField('created date')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: rename answer_text to text
    answer_text = models.CharField(max_length=200)
    # user_id = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.now())
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.answer_text


class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    created_date = models.DateTimeField('created date')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    def __str__(self):
        return self.comment_text

