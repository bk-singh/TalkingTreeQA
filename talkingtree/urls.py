from django.conf.urls import include, url
# from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
from . import views
# from django.contrib import admin
# from django.urls import path
# from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

app_name ='talkingtree'
urlpatterns = [
    # url(r'^$', views.question, name='question'),
    url(r'^$', views.QuestionView.as_view(), name='question'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # url(r'^login/$', views.login, name='login'),
    url(r'^login/$', auth_views.login, name='login'),

    # url(r'^logout/$', views.logout, name='logout'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^question/add/$', views.QuestionCreate.as_view(), name='add-question'),

    url(r'^(?P<pk>[0-9]+)/add-answer/$', views.AnswerCreate.as_view(), name='add-answer'),

    url(r'^(?P<pk>[0-9]+)/add-comment/$', views.CommentCreate.as_view(), name='add-comment'),

    url(r'^(?P<question_id>[0-9]+)/$', views.answer, name='answer'),
    # url(r'^(?P<pk>[0-9]+)/$', views.AnswerView.as_view(), name='answer'),

    url(r'^answer/(?P<answer_id>[0-9]+)/$', views.comment, name='comment'),

    url(r'^profile/$', views.your_view, name='profile'),
]
