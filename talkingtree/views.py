from django.http import HttpResponse
from django.template import loader
from .models import Question, Answer, Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.views.generic import View
from .models import Question, Answer, Comment
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



class QuestionView(generic.ListView):
    template_name = 'talkingtree/index.html'
    context_object_name = 'all_question'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.all()


class QuestionCreate(CreateView):
    model = Question
    fields = ['user_id','question_text','created_date']
    success_url = reverse_lazy('talkingtree:question')


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['user_id','question_text','created_date']
    success_url = reverse_lazy('talkingtree:question')


class QuestionDelete(DeleteView):
    model = Question
    fields = ['user_id','question_text','created_date']
    success_url = reverse_lazy('talkingtree:question')


class AnswerCreate(CreateView):
    def get_queryset(self):
        model = Answer
        question = Question.objects.get(pk=self.kwargs['pk'])
        fields = ['question', 'answer_text', 'created_date', 'upvotes', 'downvotes']
        template_name = 'talkingtree:question'
        # self.question = get_object_or_404(Question, name=self.args[0])
        return Answer.objects.filter(question=question)


class CommentCreate(CreateView):
    model = Question
    fields = ['answer','comment_text','created_date',]
    success_url = reverse_lazy('talkingtree:question')


# def question(request):
#     all_question = Question.objects.all()
#     context = { 'all_question' : all_question }
#     return render(request, 'talkingtree/index.html', context)


# class AnswerView(generic.ListView):
#     template_name = 'talkingtree/answer.html'
#     context_object_name = 'answer'
#     question = Question.objects.get(pk=question_id)
#     all_answer = Answer.objects.filter(question_id=question_id)
#     count_answer = question.answer_set.count();
#     answer = { 'question' : question, 'all_answer': all_answer, 'count_answer': count_answer }
#     def get_queryset(self):
#         return answer


# @login_required
def answer(request, question_id):
    try:

        question = Question.objects.get(pk=question_id)
        all_answer = Answer.objects.filter(question_id=question_id)
        count_answer = question.answer_set.count();
    except Question.DoesNotExist:
        raise Http404('Answer Does not Exist.')
    return render(request, 'talkingtree/answer.html', { 'question' : question, 'all_answer': all_answer, 'count_answer': count_answer })


# @login_required
def comment(request, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
        # question = Question.objects.filter(pk = question_id)
        question = Question.objects.filter(answer__id=answer_id)
        all_comment = Comment.objects.filter(answer = answer)
        count_comment = answer.comment_set.count();
    except Question.DoesNotExist:
        raise Http404('comment Does not Exist.')
    return render(request, 'talkingtree/comment.html', { 'question':question, 'answer' : answer, 'all_comment': all_comment, 'count_comment':count_comment })

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
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user.set_password(password)
            # user.first_name = 'BK'
            # user.last_name = 'Singh'
            user.save()

            user = authenticate(username='username', password='password')
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('talkingtree:question')
        return render(request, self.template_name, {'form': form })

#
# def login(request):
#     try:
#         del request.session['username']
#     except:
#         pass
#     return render(request, 'talkingtree/login.html')
#
# def logout(request):
#     try:
#         del request.session['username']
#     except:
#         pass
#     return render(request, 'talkingtree/logout.html')

def your_view(request):
    template_name = 'talkingtree/profile.html'
    a = User.objects.get(username= request.user)
     # profile = a.get_profile()
    return render(request, template_name, {'profile': a})
