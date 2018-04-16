from django.conf.urls import include, url
# from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
from . import views
# from django.contrib import admin
# from django.urls import path
# from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.admin import views as admin_views
from django.views.generic.base import TemplateView

app_name ='talkingtree'
urlpatterns = [
    # url(r'^$', views.question, name='question'),
    # url(r'^login/$', views.login, name='login'),
    # url(r'^logout/$', views.logout, name='logout'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^$', views.QuestionView.as_view(), name='question'),
    url(r'^myquestions/$', views.myquestions, name='myquestions'),
    url(r'^question/add/$', views.QuestionCreate.as_view(), name='add-question'),
    # url(r'^question/add1/$', views.QuestionCreate1.as_view(), name='add-question1'),
    url(r'^question/(?P<pk>[0-9]+)/$', views.QuestionUpdate.as_view(), name='update-question'),
    url(r'^question/(?P<pk>[0-9]+)/delete/$', views.QuestionDelete.as_view(), name='delete-question'),

    url(r'^(?P<question_id>[0-9]+)/$', views.answer, name='answer'),
    url(r'^answer/add/$', views.AnswerCreate.as_view(), name='add-answer'),
    url(r'^answer/(?P<pk>[0-9]+)/$', views.AnswerUpdate.as_view(), name='update-answer'),
    url(r'^answer/(?P<pk>[0-9]+)/delete/$', views.AnswerDelete.as_view(), name='delete-answer'),
    url(r'^myanswers/$', views.myanswers, name='myanswers'),

    url(r'^comments/(?P<answer_id>[0-9]+)/$', views.comment, name='comment'),
    url(r'^comment/(?P<pk>[0-9]+)/$', views.CommentUpdate.as_view(), name='update-comment'),
    url(r'^comment/(?P<pk>[0-9]+)/delete/$', views.CommentDelete.as_view(), name='delete-comment'),
    url(r'^comment/add/$', views.CommentCreate.as_view(), name='add-comment'),

    url(r'^answer/(?P<answer_id>[0-9]+)/upvotes_answer/$', views.create_upvoteanswer, name='upvotes_answer'),
    url(r'^answer/(?P<answer_id>[0-9]+)/downvotes_answer/$', views.create_downvoteanswer, name='downvotes_answer'),
    url(r'^answer/(?P<comment_id>[0-9]+)/upvotes_comment/$', views.create_upvotecomment, name='upvotes_comment'),
    url(r'^answer/(?P<comment_id>[0-9]+)/downvotes_comment/$', views.create_downvotecomment, name='downvotes_comment'),

    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^account/(?P<pk>[0-9]+)/$', views.UserUpdate.as_view(), name='update_user'),

    # url(r'^password-change/$', auth_views.password_change,{'post_change_redirect': 'password_change_done'}, name='password_change'),
    # url(r'^password-change-done/$', auth_views.password_change_done, name='password_change_done'),
    # url(r'^password-change/$', admin_views.password_change, {'post_change_redirect': 'password_change_done'}, name='password_change'),
    # url(r'password_change/$', admin_views.PasswordChangeView.as_view(template_name='password_change.html',    #                                                                 success_url='/accounts/password_change_done')),
    # url(r'password_change_done/', admin_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html')),
    # url(r'^(?P<pk>[0-9]+)/$', views.AnswerView.as_view(), name='answer'),

]
