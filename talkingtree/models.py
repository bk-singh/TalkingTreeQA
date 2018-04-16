from django.db import models
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import datetime
from django.contrib.auth.models import User


class Question(models.Model):
    '''
        Question model has info about questions posted by user
    '''
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    question_text = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('talkingtree:answer', kwargs={'pk':self.pk})

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    '''
        Answer model has info about answers posted by user
    '''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    answer_text = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('talkingtree:answer', kwargs={'pk':self.pk})

    def __str__(self):
        return self.answer_text


class Upvoteanswer(models.Model):
    '''
        this model has info about all the upvote/downvotes by user on a answer
    '''
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    upvote = models.NullBooleanField( null=True, blank=True, default=True)

    class Meta:
        ordering = ['-upvote']

    def __str__(self):
        return self.upvote


class Comment(models.Model):
    '''
        this model has info about comments by users on an answer
    '''
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    comment_text = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.comment_text


class Upvotecomment(models.Model):
    '''
        this model has info about all the upvote/downvotes by user on a comment
    '''
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    upvote = models.NullBooleanField( null=True, blank=True, default=None)

    class Meta:
        ordering = ['-upvote']

    def __str__(self):
        return self.upvote
