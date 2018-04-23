from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.views.generic import View
from talkingtree.models import Question, Answer, Voteanswer
from talkingtree.forms import NewAnswerForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView


class AnswerView(generic.ListView):
    template_name = 'talkingtree/index.html'
    context_object_name = 'all_answer'
    paginate_by = 5

    def get_queryset(self):
        return Answer.objects.all()


class AnswerCreate(View):
    template_name = 'talkingtree/question_form.html'
    form_class = NewAnswerForm

    def get(self, request, question_id):
        if request.user.is_authenticated:
            form = self.form_class(None)
            q = Question.objects.get(pk=question_id)
            return render(request, self.template_name, {'form': form, 'question':q})
        else:
            return redirect('talkingtree:login')

    def post(self, request, question_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            que = Question.objects.get(pk=question_id)
            answer = Answer.objects.create(user=request.user, question=que, answer_text=form.cleaned_data['answer'])
            answer.save()
        return redirect('talkingtree:answer', question_id)


class AnswerDelete(DeleteView):
    model = Answer
    fields = ['question', 'user', 'answer_text', 'created_date',]
    success_url = reverse_lazy('talkingtree:question')

class AnswerUpdate(FormView):
    template_name = 'talkingtree/question_form.html'
    form_class = NewAnswerForm

    def get(self, request, question_id, pk):
        if request.user.is_authenticated:
            answer = Answer.objects.get(pk=pk)
            question = Question.objects.get(pk=question_id)
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form, 'question': question, 'answer':answer})
        else:
            return redirect('talkingtree:login')

    def post(self, request, question_id, pk):
        form_class = NewAnswerForm
        form = self.form_class(request.POST)
        if form.is_valid():
            answer = Answer.objects.get(pk=pk)
            answer.answer_text = form.cleaned_data['answer']
            answer.save()
        return redirect('talkingtree:answer', question_id)


#
# class AnswerUpdate(UpdateView):
#     model = Answer
#     fields = ['question', 'user', 'answer_text']
#     success_url = reverse_lazy('talkingtree:question')


def answer(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        answers = Answer.objects.filter(question_id=question_id)
        count_answer = answers.count();
        answers_list = []
        for answer in answers:
            count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
            count_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
            count_uservote = None
            if request.user.is_authenticated:
                count_uservote = Voteanswer.objects.filter(user=request.user, answer=answer).count()
            if count_uservote > 0:
                uservote = Voteanswer.objects.filter(user=request.user, answer=answer).first()
                answers_list.append({
                    'answer': answer,
                    'vote': uservote.vote,
                    'count_upvoteanswer': count_upvote,
                    'count_downvoteanswer': count_downvote
                })
            else:
                answers_list.append({
                    'answer':answer,
                    'vote': None,
                    'count_upvoteanswer':count_upvote,
                    'count_downvoteanswer':count_downvote
                })
    except Question.DoesNotExist:
        raise Http404('Answer Does not Exist.')
    return render(request, 'talkingtree/answer.html', {
        'question' : question, 'all_answer': answers_list, 'count_answer': count_answer,})


@login_required
def myanswers(request):
    try:
        answers = Answer.objects.filter(user=request.user)
        count_answer = answers.count()
        answers_list = []
        for answer in answers:
            count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
            count_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
            answers_list.append({
                'answer':answer,
                'count_upvoteanswer':count_upvote,
                'count_downvoteanswer':count_downvote
            })

    except Question.DoesNotExist:
        raise Http404('Answer Does not Exist.')
    return render(request, 'talkingtree/myanswers.html', {
       'all_answer': answers_list, 'count_answer': count_answer,})

