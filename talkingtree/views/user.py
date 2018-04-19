from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.views.generic import View
from talkingtree.forms import UserForm
from django.contrib.auth.models import User


# User registration/Authentication
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

