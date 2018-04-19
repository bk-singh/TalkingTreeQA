from django.conf.urls import url
# from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
# from talkingtree.views import views
# from . import views

from talkingtree.views import user, question, answer, voteanswer, comment, votecomment

# from django.contrib import admin
# from django.urls import path
# from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

app_name ='talkingtree'
urlpatterns = [

    url(r'^register/$', user.UserFormView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^$', question.QuestionView.as_view(), name='question'),
    url(r'^myquestions/$', question.myquestions, name='myquestions'),
    url(r'^question/add/$', question.QuestionCreate.as_view(), name='add-question'),
    url(r'^questions/(?P<pk>[0-9]+)/update$', question.QuestionUpdate.as_view(), name='update-question'),
    url(r'^questions/(?P<pk>[0-9]+)/delete/$', question.QuestionDelete.as_view(), name='delete-question'),

    url(r'^questions/(?P<question_id>[0-9]+)/answers/$', answer.answer, name='answer'),
    url(r'^questions/(?P<question_id>[0-9]+)/answers/add/$', answer.AnswerCreate.as_view(), name='add-answer'),
    url(r'^questions/(?P<question_id>[0-9]+)/answers/(?P<pk>[0-9]+)/update$', answer.AnswerUpdate.as_view(), name='update-answer'),
    url(r'^questions/(?P<question_id>[0-9]+)/answers/(?P<pk>[0-9]+)/delete/$', answer.AnswerDelete.as_view(), name='delete-answer'),
    url(r'^myanswers/$', answer.myanswers, name='myanswers'),

    url(r'^questions/(?P<question_id>[0-9]+)/answers/(?P<answer_id>[0-9]+)/comments/$', comment.comment, name='comment'),
    url(r'^questions/(?P<question_id>[0-9]+)/answers/(?P<answer_id>[0-9]+)/comments/(?P<pk>[0-9]+)/update$', comment.CommentUpdate.as_view(), name='update-comment'),
    url(r'^questions/(?P<question_id>[0-9]+)/answers/(?P<answer_id>[0-9]+)/comments/(?P<pk>[0-9]+)/delete/$', comment.CommentDelete.as_view(), name='delete-comment'),
    url(r'^questions/(?P<question_id>[0-9]+)/answers/(?P<answer_id>[0-9]+)/comments/add/$', comment.CommentCreate.as_view(), name='add-comment'),

    url(r'^answer/(?P<answer_id>[0-9]+)/upvotes_answer/$', voteanswer.create_voteanswer, name='upvotes_answer'),
    url(r'^answer/(?P<answer_id>[0-9]+)/downvotes_answer/$', voteanswer.create_downvoteanswer, name='downvotes_answer'),

    url(r'^answer/(?P<comment_id>[0-9]+)/upvotes_comment/$', votecomment.create_votecomment, name='upvotes_comment'),
    url(r'^answer/(?P<comment_id>[0-9]+)/downvotes_comment/$', votecomment.create_downvotecomment, name='downvotes_comment'),

    url(r'^account/profile/$', user.profile_view, name='profile'),
    url(r'^account/profile/(?P<pk>[0-9]+)/update$', user.UserUpdate.as_view(), name='update_user'),
]
