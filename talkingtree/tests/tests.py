
from __future__ import unicode_literals
from django.test import TestCase, Client, RequestFactory
from talkingtree.models import Question, Answer, Comment, Voteanswer, Votecomment
from django.contrib.auth.models import User, AnonymousUser
from datetime import datetime
from django.core.urlresolvers import reverse
from talkingtree.views import user, question, answer, voteanswer, comment, votecomment
# from django.contrib.auth import views as auth_views
# from django.shortcuts import reverse

# import pytest


def create_user( username, email = 'test@gmail.com', password = 'test'):
    user = User.objects.create_user(username=username, email=email, password=password)
    return user


def get_user_by_username(username):
    return User.objects.filter(username=username).first()


def create_question(question_text, user):
        return Question.objects.create(question_text=question_text, user= user, created_date= datetime.now())


def create_answer(answer_text, question, user):
        return Answer.objects.create(answer_text=answer_text, question=question, user= user, created_date= datetime.now())


def create_comment(comment_text, answer, user):
        return Comment.objects.create(comment_text= comment_text, answer=answer, user= user, created_date= datetime.now())


class QuestionTest(TestCase):
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.factory = RequestFactory()
        self.client = Client()
        self.user = create_user('test', 'test@gmail.com', 'test')

    def test_question_creation(self):
        ''' Test updating a question. '''
        # q = create_question("How can I fly over the mountain?", self.user);
        url = reverse('talkingtree:add-question')
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        form = {'question':"What is Airport??"}
        resp1 = self.client.post(url, form)

        q1 = Question.objects.all().first()
        url = reverse('talkingtree:question')
        resp2 = self.client.get(url)

        self.assertEqual(form['question'], q1.question_text)
        self.assertEqual(resp1.status_code, 302)
        self.assertIn(q1.question_text, resp2.content)

    def test_question_view_allowed_anonymous_user(self):
        q = create_question("How can I fly over the mountain?", self.user);

        url = reverse('talkingtree:question')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(q.question_text, resp.content)
        self.assertTemplateUsed(resp, 'talkingtree/index.html')

    def test_question_view_allowed_loggedin_user(self):
        q = create_question("How can I fly over the mountain?", self.user);
        url = reverse('talkingtree:question')
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(q.question_text, resp.content)
        self.assertTemplateUsed(resp, 'talkingtree/index.html')

    def test_delete_question_by_loggedin_user(self):
        q = create_question("How can I fly over the mountain?", self.user);
        url = reverse('talkingtree:delete-question', kwargs={'pk': q.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        url = reverse('talkingtree:question')
        resp2 = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(q.question_text, resp.content)
        self.assertTemplateUsed(resp, 'talkingtree/question_confirm_delete.html')
        # self.assertNotIn(q.question_text, resp2.content)

    def test_update_question_by_loggedin_user(self):
        ''' Test updating a question. '''
        q = create_question("How can I fly over the mountain?", self.user);
        url = reverse('talkingtree:update-question', kwargs={'pk':q.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        form = {'question':" What is Airport??"}
        resp1 = self.client.post(url, form)
        q1 = Question.objects.get(pk=q.id)
        url = reverse('talkingtree:question')
        resp2 = self.client.get(url)
        self.assertEqual(resp1.status_code, 302)
        self.assertIn(q1.question_text, resp2.content)
        self.assertNotIn(q.question_text, resp2.content)


class AnswerTest(TestCase):
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.factory = RequestFactory()
        self.client = Client()
        self.user = create_user('test', 'test@gmail.com', 'test')

    def test_answer_view_allowed_anonymous_user(self):
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);

        url = '/talkingtree/questions/'+ str(q.id) + '/answers/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(q.question_text, resp.content)
        self.assertIn(a.answer_text, resp.content)
        self.assertTemplateUsed(resp, 'talkingtree/answer.html')

    def test_answer_view_allowed_loggedin_user(self):
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);

        url = '/talkingtree/questions/'+ str(q.id) + '/answers/'
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(q.question_text, resp.content)
        self.assertIn(a.answer_text, resp.content)
        self.assertTemplateUsed(resp, 'talkingtree/answer.html')

    def test_delete_answer_by_loggedin_user(self):
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);

        url = reverse('talkingtree:delete-answer', kwargs={'question_id': q.id, 'pk': a.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)

        url = reverse('talkingtree:answer', kwargs={'question_id': q.id})
        resp2 = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # self.assertNotIn(a.answer_text, resp2.content)

    def test_update_answer_by_loggedin_user(self):
        ''' Test updating a answer. '''
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);
        url = reverse('talkingtree:update-answer', kwargs={'question_id': q.id, 'pk': a.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        form = {'answer':"Parachute is just another option."}
        resp1 = self.client.post(url, form)
        a1 = Answer.objects.get(pk=a.id)
        url = reverse('talkingtree:answer', kwargs= {'question_id': q.id})
        resp2 = self.client.get(url)
        self.assertEqual(resp1.status_code, 302)
        self.assertIn(a1.answer_text, resp2.content)
        self.assertNotIn(a.answer_text, resp2.content)


class CommentTest(TestCase):
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.factory = RequestFactory()
        self.client = Client()
        self.user = create_user('test', 'test@gmail.com', 'test')

    def test_comment_view_allowed_anonymous_user(self):
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);
        c = create_comment("There is no airport in this region and  I cannot use parachute because wind speed is too much.", a, self.user)

        url = '/talkingtree/questions/' + str(q.id) + '/answers/'+ str(a.id) + '/comments/'
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(q.question_text, resp.content)
        self.assertIn(a.answer_text, resp.content)
        self.assertIn(c.comment_text, resp.content)
        self.assertTemplateUsed(resp, 'talkingtree/comment.html')

    def test_comment_view_allowed_loggedin_user(self):
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);
        c = create_comment("There is no airport in this region and  I cannot use parachute because wind speed is too much.", a, self.user)

        url = '/talkingtree/questions/' + str(q.id) + '/answers/'+ str(a.id) + '/comments/'
        self.client.login(username='test', password='test')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(q.question_text, resp.content)
        self.assertIn(a.answer_text, resp.content)
        self.assertIn(c.comment_text, resp.content)
        self.assertTemplateUsed(resp, 'talkingtree/comment.html')

    def test_delete_comment_by_loggedin_user(self):
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);
        c = create_comment("I cannot by an Aeroplane. ", a, self.user)
        url = reverse('talkingtree:delete-comment', kwargs={'question_id': q.id,'answer_id': a.id, 'pk': a.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_update_comment_by_loggedin_user(self):
        ''' Test updating a answer. '''
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);
        c = create_comment("I cannot buy an Aeroplane. ", a, self.user)

        url = reverse('talkingtree:update-comment', kwargs={'question_id': q.id,'answer_id': a.id, 'pk': a.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        form = {'comment':"though Parachute is good option"}
        resp1 = self.client.post(url, form)
        c1 = Comment.objects.get(pk=c.id)
        url = reverse('talkingtree:comment', kwargs= {'question_id': q.id, 'answer_id': a.id})
        resp2 = self.client.get(url)
        self.assertEqual(resp1.status_code, 302)
        self.assertIn(c1.comment_text, resp2.content)
        self.assertNotIn(c.comment_text, resp2.content)


class LoginTest(TestCase):
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.factory = RequestFactory()
        self.client = Client()
        self.user = create_user('test', 'test@gmail.com', 'test')

    def test_login_view_allowed_anonymous_user(self):
        url = '/talkingtree/login/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class UserTest(TestCase):
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.factory = RequestFactory()
        self.client = Client()
        self.user = create_user('test', 'test@gmail.com', 'test')

    def test_register_page_access_to_anonymous_user(self):
        url = '/talkingtree/register/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.content)
        self.assertIn('password', response.content)
        self.assertIn('email', response.content)

    def test_register_a_new_user(self):
        url = '/talkingtree/register/'
        form = {'username':'testuser', 'password':'testuser', 'email':'testuser@gmail.com'}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.login(username=form['username'], password=form['password']))

    def test_user_profile(self):
        template_name = 'talkingtree/profile.html'
        form = {'username':'test', 'password':'test', 'email':'test@gmail.com'}
        request = self.factory.get(reverse('talkingtree:profile'))
        request.user = self.user
        response =  user.profile_view(request)
        userprofile = User.objects.get(username=form['username'])
        self.assertEqual(response.status_code, 200)

class AnswervoteTest(TestCase):
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.factory = RequestFactory()
        self.client = Client()
        self.user = create_user('test', 'test@gmail.com', 'test')

    def test_upvote_answer(self):
        ''' Test upvote  an answer for the first time. '''
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);

        url = reverse('talkingtree:upvotes_answer', kwargs={'answer_id': a.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        # resp = self.client.get(url)
        count_upvote = Voteanswer.objects.filter(vote=True, answer=a).count()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count_upvote, 1)

    def test_downvote_answer(self):
        ''' Test downvote  an answer for first time. '''
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);

        url = reverse('talkingtree:downvotes_answer', kwargs={'answer_id': a.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        # resp = self.client.get(url)
        count_downvote = Voteanswer.objects.filter(vote=False, answer=a).count()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count_downvote, 1)

    def test_upvote_answer_model(self):
        ''' Test Voteanswer model '''
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);
        c = create_comment("I cannot buy an Aeroplane. ", a, self.user)
        avote = Voteanswer(vote=None, user=self.user, answer=a)

        vote = avote.save_vote(True)
        assert vote == True
        count_upvote = Voteanswer.objects.filter(vote=True, answer=a).count()
        self.assertEqual(count_upvote, 1)

        vote = avote.save_vote(True)
        assert vote == None
        count_upvote = Voteanswer.objects.filter(vote=True, answer=a).count()
        self.assertEqual(count_upvote, 0)

        vote = avote.save_vote(False)
        assert vote == False
        count_downvote = Voteanswer.objects.filter(vote=False, answer=a).count()
        self.assertEqual(count_downvote, 1)

        vote = avote.save_vote(False)
        assert vote == None
        count_downvote = Voteanswer.objects.filter(vote=False, answer=a).count()
        self.assertEqual(count_downvote, 0)



class CommentvoteTest(TestCase):
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.factory = RequestFactory()
        self.client = Client()
        self.user = create_user('test', 'test@gmail.com', 'test')

    def test_upvote_comment(self):
        ''' Test upvote  a comment for the first time. '''
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);
        c = create_comment("I cannot by an Aeroplane. ", a, self.user)

        url = reverse('talkingtree:upvotes_comment', kwargs={'comment_id': c.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        resp = self.client.get(url)
        count_upvote = Votecomment.objects.filter(vote=True, comment=c).count()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count_upvote, 0)

    def test_downvote_comment(self):
        ''' Test downvote  a comment for first time. '''
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);
        c = create_comment("I cannot by an Aeroplane. ", a, self.user)

        url = reverse('talkingtree:downvotes_comment', kwargs={'comment_id': c.id})
        self.client.login(username='test', password='test')
        resp = self.client.get(url)
        resp = self.client.get(url)
        count_downvote = Votecomment.objects.filter(vote=False, comment=c).count()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count_downvote, 0)



    def test_upvote_comment_model(self):
        ''' Test Votecomment model '''
        q = create_question("How can I fly over the mountain?", self.user);
        a = create_answer("You can use Parachute or Aeroplane.", q, self.user);
        c = create_comment("I cannot by an Aeroplane. ", a, self.user)
        cvote = Votecomment(vote=None, user=self.user, comment=c)

        vote = cvote.save_vote(True)
        assert vote == True
        count_upvote = Votecomment.objects.filter(vote=True, comment=c).count()
        self.assertEqual(count_upvote, 1)

        vote = cvote.save_vote(True)
        assert vote == None
        count_upvote = Votecomment.objects.filter(vote=True, comment=c).count()
        self.assertEqual(count_upvote, 0)

        vote = cvote.save_vote(False)
        assert vote == False
        count_upvote = Votecomment.objects.filter(vote=False, comment=c).count()
        self.assertEqual(count_upvote, 1)

        vote = cvote.save_vote(False)
        assert vote == None
        count_upvote = Votecomment.objects.filter(vote=False, comment=c).count()
        self.assertEqual(count_upvote, 0)


