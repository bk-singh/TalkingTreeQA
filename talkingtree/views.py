from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.views.generic import View
from .models import Question, Answer, Comment, Upvoteanswer, Upvotecomment
from .forms import UserForm, NewQuestionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect


class QuestionView(generic.ListView):
    template_name = 'talkingtree/index.html'
    context_object_name = 'all_question'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.all()


class QuestionCreate(CreateView):
    model = Question
    fields = ['user', 'question_text']
    success_url = reverse_lazy('talkingtree:question')


class QuestionCreate1(View):

    def get(self, request):
        form = NewQuestionForm()
        variables = RequestContext(request, {'form': form, 'request':request})
        return render_to_response('talkingtree/question_form.html', {'form': form, 'request':request})

    @method_decorator(csrf_protect, name='dispatch')
    def post(self, request):
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question = Question.objects.create(user=request.user,question_text = form.cleaned_data['question_text'])
        return render(request, 'talkingtree/',)


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['user','question_text']
    success_url = reverse_lazy('talkingtree:question')


class QuestionDelete(DeleteView):
    model = Question
    fields = ['user','question_text']
    success_url = reverse_lazy('talkingtree:question')


class AnswerView(generic.ListView):
    template_name = 'talkingtree/index.html'
    context_object_name = 'all_answer'
    paginate_by = 5

    def get_queryset(self):
        return Answer.objects.all()


class AnswerCreate(CreateView):
    model = Answer
    fields = ['question', 'user', 'answer_text']
    success_url = reverse_lazy('talkingtree:question')


class AnswerDelete(DeleteView):
    model = Answer
    fields = ['question', 'user', 'answer_text', 'created_date', 'upvotes', 'downvotes']
    success_url = reverse_lazy('talkingtree:question')


class AnswerUpdate(UpdateView):
    model = Answer
    fields = ['question', 'user', 'answer_text']
    success_url = reverse_lazy('talkingtree:question')


class CommentCreate(CreateView):
    model = Comment
    fields = ['answer', 'user', 'comment_text',]
    success_url = reverse_lazy('talkingtree:question')


class CommentDelete(DeleteView):
    model = Comment
    fields = ['answer', 'user', 'comment_text','created_date',]
    success_url = reverse_lazy('talkingtree:question')


class CommentUpdate(UpdateView):
    model = Comment
    fields = ['answer', 'user', 'comment_text',]
    success_url = reverse_lazy('talkingtree:question')


def answer(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        all_answer = Answer.objects.filter(question_id=question_id)
        count_answer = question.answer_set.count();
        count_upvoteanswer = Upvoteanswer.objects.filter(upvote=True).count()
        count_downvoteanswer = Upvoteanswer.objects.filter(upvote=False).count()
        answers = []
        for item in all_answer:
            count_upvoteanswer = Upvoteanswer.objects.filter(upvote=True, answer=item).count()
            count_downvoteanswer = Upvoteanswer.objects.filter(upvote=False, answer=item).count()
            answers.append({
                'answer':item,
                'count_upvoteanswer':count_upvoteanswer,
                'count_downvoteanswer':count_downvoteanswer
            })

    except Question.DoesNotExist:
        raise Http404('Answer Does not Exist.')
    return render(request, 'talkingtree/answer.html', {
        'question' : question, 'all_answer': answers, 'count_answer': count_answer, 'count_upvoteanswer': count_upvoteanswer ,'count_downvoteanswer':count_downvoteanswer})


@login_required
def myanswers(request):
    try:
        all_answer = Answer.objects.filter(user=request.user)
        count_answer = all_answer.count()
        answers = []
        for item in all_answer:
            count_upvoteanswer = Upvoteanswer.objects.filter(upvote=True, answer=item).count()
            count_downvoteanswer = Upvoteanswer.objects.filter(upvote=False, answer=item).count()
            answers.append({
                'answer':item,
                'count_upvoteanswer':count_upvoteanswer,
                'count_downvoteanswer':count_downvoteanswer
            })

    except Question.DoesNotExist:
        raise Http404('Answer Does not Exist.')
    return render(request, 'talkingtree/myanswers.html', {
       'all_answer': answers, 'count_answer': count_answer, 'count_upvoteanswer': count_upvoteanswer ,'count_downvoteanswer':count_downvoteanswer})


@login_required
def myquestions(request):
    try:
        all_questions = Question.objects.filter(user=request.user)
        count_question= all_questions.count()

    except Question.DoesNotExist:
        raise Http404('Answer Does not Exist.')
    return render(request, 'talkingtree/myquestions.html', {
       'all_questions': all_questions, 'count_question': count_question,})


@login_required
def create_answer(request, question_id):
    user = get_object_or_404(User, username=request.user)
    question = get_object_or_404(Question, pk=question_id)
    answer_text= 'ans from backend'
    try:
        question = Question.objects.get(answer__id=answer_id)
        answer = Answer.objects.get(user = user, question=question)
    except Answer.DoesNotExist:
        answer = Answer(upvote=True, user = user, question=question, answer_text=answer_text)
        answer.save()
    return redirect('talkingtree:question')



@login_required
def create_upvoteanswer(request, answer_id):
    user = get_object_or_404(User, username=request.user)
    answer = get_object_or_404(Answer, pk=answer_id)
    try:
        question = Question.objects.get(answer__id=answer_id)
        upvoteanswer = Upvoteanswer.objects.get(user = user, answer=answer)
        if(upvoteanswer.upvote == True):
            upvoteanswer.upvote = None
        else:
            upvoteanswer.upvote = True
        upvoteanswer.save()
    except Upvoteanswer.DoesNotExist:
        upvoteanswer = Upvoteanswer(upvote=True, user = user, answer=answer)
        upvoteanswer.save()
    return redirect('talkingtree:answer', question.id)


@login_required
def create_downvoteanswer(request, answer_id):
    user = get_object_or_404(User, username=request.user)
    answer = get_object_or_404(Answer, pk=answer_id)
    try:
        question = Question.objects.get(answer__id=answer_id)
        upvoteanswer = Upvoteanswer.objects.get(user = user, answer=answer)
        if(upvoteanswer.upvote == False):
            upvoteanswer.upvote = None
        else:
            upvoteanswer.upvote = False
        upvoteanswer.save()
    except Upvoteanswer.DoesNotExist:
        upvoteanswer = Upvoteanswer(upvote=False, user = user, answer=answer)
        upvoteanswer.save()
    return redirect('talkingtree:answer', question.id)


# @login_required
def comment(request, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
        # question = Question.objects.filter(pk = question_id)
        question = Question.objects.filter(answer__id=answer_id)
        all_comment = Comment.objects.filter(answer = answer)
        count_comment = answer.comment_set.count();
        comments = []
        for item in all_comment:
            count_upvotecomment = Upvotecomment.objects.filter(upvote=True, comment=item).count()
            count_downvotecomment = Upvotecomment.objects.filter(upvote=False, comment=item).count()
            comments.append({
                'comment':item,
                'count_upvotecomment':count_upvotecomment,
                'count_downvotecomment':count_downvotecomment
            })

    except Question.DoesNotExist:
        raise Http404('comment Does not Exist.')
    return render(request, 'talkingtree/comment.html', { 'question':question, 'answer' : answer,
                                                         'all_comment': comments, 'count_comment':count_comment,
                                                         })


@login_required
def create_upvotecomment(request, comment_id):
    user = get_object_or_404(User, username=request.user)
    comment = get_object_or_404(Comment, pk=comment_id)
    try:
        answer = Answer.objects.get(comment__id=comment_id)
        upvotecomment = Upvotecomment.objects.get(user = user, comment=comment)
        if(upvotecomment.upvote == True):
            upvotecomment.upvote = None;
        else:
            upvotecomment.upvote = True
        upvotecomment.save()
    except Upvotecomment.DoesNotExist:
        upvotecomment = Upvotecomment(upvote=True, user = user, comment=comment)
        upvotecomment.save()
    return redirect('talkingtree:comment', answer.id)


@login_required
def create_downvotecomment(request, comment_id):
    user = get_object_or_404(User, username=request.user)
    comment = get_object_or_404(Comment, pk=comment_id)
    try:
        answer = Answer.objects.get(comment__id=comment_id)
        upvotecomment = Upvotecomment.objects.get(user = user, comment=comment)
        if(upvotecomment.upvote == False):
            upvotecomment.upvote = None
        else:
            upvotecomment.upvote = False
        upvotecomment.save()
    except Upvotecomment.DoesNotExist:
        upvotecomment = Upvotecomment(upvote=False, user = user, comment=comment)
        upvotecomment.save()
    return redirect('talkingtree:comment', answer.id)


# User Authentication
class UserFormView(View):
    form_class = UserForm
    template_name = 'talkingtree/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username='username', password='password')
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('talkingtree:question')
        return redirect('talkingtree:login')


class UserUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username',]
    template_name = 'talkingtree/user_update.html'
    slug_field = 'username'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('talkingtree:profile')


def profile_view(request):
    template_name = 'talkingtree/profile.html'
    a = User.objects.get(username= request.user)
    return render(request, template_name, {'profile': a})

