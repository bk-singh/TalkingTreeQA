from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View
from talkingtree.models import Question
from talkingtree.forms import UserForm, NewQuestionForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView




class QuestionView(generic.ListView):
    template_name = 'talkingtree/index.html'
    context_object_name = 'all_question'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.all()


class QuestionCreate(View):
    template_name = 'talkingtree/question_form.html'
    form_class = NewQuestionForm

    def get(self, request):
        if request.user.is_authenticated:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('talkingtree:login')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            question = Question.objects.create(user=request.user, question_text=form.cleaned_data['question'])
            question.save()
        return redirect('talkingtree:question')


class QuestionUpdate(FormView):
    template_name = 'talkingtree/question_form.html'
    form_class = NewQuestionForm

    def get(self, request, pk):
        if request.user.is_authenticated:
            question = Question.objects.get(pk=pk)
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form, 'question':question})
        else:
            return redirect('talkingtree:login')

    def post(self, request, pk):
        form_class = NewQuestionForm
        form = self.form_class(request.POST)
        if form.is_valid():
            question = Question.objects.get(pk=pk)
            question.question_text = form.cleaned_data['question']
            question.save()
        return redirect('talkingtree:question')


class QuestionDelete(DeleteView):
    model = Question
    fields = ['user','question_text']
    success_url = reverse_lazy('talkingtree:question')



@login_required
def myquestions(request):
    try:
        questions = Question.objects.filter(user=request.user)
        count_question= questions.count()

    except Question.DoesNotExist:
        raise Http404('Answer Does not Exist.')
    return render(request, 'talkingtree/myquestions.html', {
       'all_questions': questions, 'count_question': count_question,})

