from django.shortcuts import render, get_object_or_404, redirect
from talkingtree.models import Question, Answer, Comment, Votecomment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# @login_required
# def create_votecomment(request, comment_id):
#     user = get_object_or_404(User, username=request.user)
#     comment = get_object_or_404(Comment, pk=comment_id)
#
#     try:
#         answer = Answer.objects.get(comment__id=comment_id)
#         votecomment = Votecomment.objects.get(user = user, comment=comment)
#         if(votecomment.vote == True):
#             votecomment.vote = None;
#         else:
#             votecomment.vote = True
#         votecomment.save()
#     except Votecomment.DoesNotExist:
#         votecomment = Votecomment(vote=True, user = user, comment=comment)
#         votecomment.save()
#     return redirect('talkingtree:comment', answer.question.id, answer.id)



@login_required
def create_votecomment(request, comment_id):
    user = get_object_or_404(User, username=request.user)
    comment = get_object_or_404(Comment, pk=comment_id)
    try:
        votecomment = Votecomment.objects.get(user=user, comment=comment)
    except Votecomment.DoesNotExist:
            votecomment = Votecomment(vote=None, user = user, comment=comment)
    finally:
        votecomment.save_vote(True)
    return redirect('talkingtree:comment', votecomment.comment.answer.question.id, votecomment.comment.answer.id)


@login_required
def create_downvotecomment(request, comment_id):
    user = get_object_or_404(User, username=request.user)
    comment = get_object_or_404(Comment, pk=comment_id)
    try:
        votecomment = Votecomment.objects.get(user = user, comment=comment)
    except Votecomment.DoesNotExist:
        votecomment = Votecomment(vote=None, user=user, comment=comment)
    finally:
        votecomment.save_vote(False)
    return redirect('talkingtree:comment',  votecomment.comment.answer.question.id, votecomment.comment.answer.id)


