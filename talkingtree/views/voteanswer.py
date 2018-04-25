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
    except Voteanswer.DoesNotExist:
        voteanswer = Voteanswer(vote=None, user = user, answer=answer)
    finally:
        voteanswer.save_vote(True)
    return redirect('talkingtree:answer', question.id)


@login_required
def create_downvoteanswer(request, answer_id):
    user = get_object_or_404(User, username=request.user)
    answer = get_object_or_404(Answer, pk=answer_id)
    try:
        question = Question.objects.get(answer__id=answer_id)
        voteanswer = Voteanswer.objects.get(user = user, answer=answer)
    except Voteanswer.DoesNotExist:
        voteanswer = Voteanswer(vote=None, user = user, answer=answer)
    finally:
        voteanswer.save_vote(False)
    return redirect('talkingtree:answer', question.id)
