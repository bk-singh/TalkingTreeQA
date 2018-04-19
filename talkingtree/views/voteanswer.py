from django.shortcuts import render, get_object_or_404, redirect
from talkingtree.models import Question, Answer, Voteanswer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def create_voteanswer(request, answer_id):
    user = get_object_or_404(User, username=request.user)
    answer = get_object_or_404(Answer, pk=answer_id)
    try:
        question = Question.objects.get(answer__id=answer_id)
        voteanswer = Voteanswer.objects.get(user = user, answer=answer)
        if(voteanswer.vote == True):
            voteanswer.vote = None
        else:
            voteanswer.vote = True
        voteanswer.save()
    except Voteanswer.DoesNotExist:
        voteanswer = Voteanswer(vote=True, user = user, answer=answer)
        voteanswer.save()
    return redirect('talkingtree:answer', question.id)


@login_required
def create_downvoteanswer(request, answer_id):
    user = get_object_or_404(User, username=request.user)
    answer = get_object_or_404(Answer, pk=answer_id)
    try:
        question = Question.objects.get(answer__id=answer_id)
        voteanswer = Voteanswer.objects.get(user = user, answer=answer)
        if(voteanswer.vote == False):
            voteanswer.vote = None
        else:
            voteanswer.vote = False
        voteanswer.save()
    except Voteanswer.DoesNotExist:
        voteanswer = Voteanswer(vote=False, user = user, answer=answer)
        voteanswer.save()
    return redirect('talkingtree:answer', question.id)