from talkingtree.models import Comment, Votecomment
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View
from talkingtree.models import Question, Answer
from talkingtree.forms import NewCommentForm
from django.views.generic.edit import FormView

# class CommentCreate(CreateView):
#     model = Comment
#     fields = ['answer', 'user', 'comment_text',]
#     success_url = reverse_lazy('talkingtree:question')


class CommentCreate(View):
    template_name = 'talkingtree/question_form.html'
    form_class = NewCommentForm

    def get(self, request, question_id, answer_id):
        if request.user.is_authenticated:
            form = self.form_class(None)
            q = Question.objects.get(pk=question_id)
            a = Answer.objects.get(pk=answer_id)
            return render(request, self.template_name, {'form': form, 'question': q, 'answer': a})
        else:
            return redirect('talkingtree:login')

    def post(self, request, question_id, answer_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            # que = Question.objects.get(pk=question_id)
            ans = Answer.objects.get(pk=answer_id)
            comment = Comment.objects.create(user=request.user, answer=ans, comment_text=form.cleaned_data['comment'])
            comment.save()
        return redirect('talkingtree:comment', question_id, answer_id)



class CommentDelete(DeleteView):
    model = Comment
    fields = ['answer', 'user', 'comment_text','created_date',]
    success_url = reverse_lazy('talkingtree:question')


class CommentUpdate(FormView):
    template_name = 'talkingtree/question_form.html'
    form_class = NewCommentForm

    def get(self, request, question_id, answer_id, pk):
        if request.user.is_authenticated:
            comment = Comment.objects.get(pk=pk)
            answer = Answer.objects.get(pk=answer_id)
            question = Question.objects.get(pk=question_id)
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form,'question': question, 'answer':answer, 'comment':comment})
        else:
            return redirect('talkingtree:login')

    def post(self, request, question_id, answer_id, pk):
        form_class = NewCommentForm
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = Comment.objects.get(pk=pk)
            answer = Answer.objects.get(pk=answer_id)
            question = Question.objects.get(pk=question_id)
            comment.comment_text = form.cleaned_data['comment']
            comment.save()
        return redirect('talkingtree:comment', question_id, answer_id, )

# class CommentUpdate(UpdateView):
#     model = Comment
#     fields = ['answer', 'user', 'comment_text',]
#     success_url = reverse_lazy('talkingtree:question')
#


# @login_required

def comment(request, question_id, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
        # question = Question.objects.filter(pk = question_id)
        question = Question.objects.filter(answer__id=answer_id).first()
        comments = Comment.objects.filter(answer = answer)
        count_comment = answer.comment_set.count();
        comments_list = []

        for comment in comments:
            count_votecomment = Votecomment.objects.filter(vote=True, comment=comment).count()
            count_downvotecomment = Votecomment.objects.filter(vote=False, comment=comment).count()
            count_uservotecomment = Votecomment.objects.filter(user=request.user, comment=comment).count()
            if(count_uservotecomment > 0):
                votecomment = Votecomment.objects.filter(user=request.user, comment=comment).first()
                comments_list.append(
                    {
                        'comment': comment,
                        'vote': votecomment.vote,
                        'count_upvotecomment': count_votecomment,
                        'count_downvotecomment': count_downvotecomment
                    }
                )
            else:
                comments_list.append(
                    {
                        'comment': comment,
                        'vote': None,
                        'count_upvotecomment': count_votecomment,
                        'count_downvotecomment': count_downvotecomment
                    }
                )
    except Question.DoesNotExist:
        raise Http404('comment Does not Exist.')
    return render(request, 'talkingtree/comment.html', {'question':question, 'answer' : answer,
                                                         'all_comment': comments_list, 'count_comment':count_comment,
                                                        })
