import pytest
from django.db import IntegrityError
from talkingtree.models import Question, Answer, Comment, Voteanswer, Votecomment
from django.contrib.auth.models import User, AnonymousUser
from talkingtree.views import user, question, answer, voteanswer, comment, votecomment
from django.utils import timezone

@pytest.fixture()
def user():
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    return user

@pytest.fixture()
def question(user):
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    return question

@pytest.fixture()
def answer(question, user):
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    return answer


@pytest.mark.django_db
def test_create_a_question(user):
    '''
    test_create_a_question
    '''
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    question1 = Question.objects.get(pk=question.id)
    assert isinstance(question, Question)
    assert question1 == question

@pytest.mark.django_db
def test_update_an_existing_question(question, user):
    '''
    test_update_an_existing_question
    '''
    # question = Question.objects.create(question_text="question before update?", user=user, created_date=timezone.now())
    # question.save()
    question.question_text = "question after update?"
    question.save()
    question1 = Question.objects.get(pk=question.id)
    assert isinstance(question, Question)
    assert question1.question_text == question.question_text
    assert question1.question_text == "question after update?"

@pytest.mark.django_db
def test_delete_an_existing_question(question, user):
    '''
    test_delete_an_existing_question
    '''
    # user = User(username='test', password='test', email='test@test.com')
    # user.save()
    # question = Question.objects.create(question_text="question before update?", user=user, created_date=timezone.now())
    # question.save()

    question.delete()
    with pytest.raises(Question.DoesNotExist):
        question1 = Question.objects.get(pk=question.id)


@pytest.mark.django_db
def test_create_an_answer(question, answer, user):
    '''
    test_create_an_answer
    '''
    # user = User(username='test', password='test', email='test@test.com')
    # user.save()
    # question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    # question.save()
    # answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    # answer.save()

    answer1 = Answer.objects.get(pk=answer.id)
    assert isinstance(answer, Answer)
    assert answer1 == answer


@pytest.mark.django_db
def test_new_answer_missing_question_raises_IntegrityError(question, user):
    '''
    test_new_answer_missing_question_raises_IntegrityError
    '''
    # user = User(username='test', password='test', email='test@test.com')
    # user.save()
    # question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    # question.save()
    with pytest.raises(IntegrityError):
        answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=None, user=user, created_date=timezone.now())
        answer.save()


@pytest.mark.django_db
def test_create_a_comment(question, answer, user):
    '''
    test_create_a_comment
    '''
    # user = User(username='test', password='test', email='test@test.com')
    # user.save()
    # question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    # question.save()
    # answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    # answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    comment1 = Comment.objects.get(pk=comment.id)
    assert isinstance(comment, Comment)
    assert comment1 == comment


@pytest.mark.django_db
def test_new_comment_missing_answer_raises_IntegrityError():
    '''
    test_new_comment_missing_answer_raises_IntegrityError
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()

    with pytest.raises(IntegrityError):
        comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=None, user=user,
                                         created_date=timezone.now())
        comment.save()




@pytest.mark.django_db
def test_upvote_when_user_create_new_vote_for_upvote():
    '''
    test_upvote_when_user_create_new_vote_for_upvote
    '''

    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(True)
    assert vote == True
    assert avote.vote == True

@pytest.mark.django_db
def test_upvote_when_user_change_vote_from_none_to_upvote():
    '''
    test_upvote_when_user_change_vote_from_none_to_upvote
    '''

    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(True)
    assert vote == True
    assert avote.vote == True

@pytest.mark.django_db
def test_upvote_when_user_change_vote_from_downvote_to_upvote():
    '''
    test_upvote_when_user_change_vote_from_downvote_to_upvote
    '''

    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(True)
    assert vote == True
    assert avote.vote == True



@pytest.mark.django_db
def test_upvote_when_user_change_vote_from_upvote_to_None	():
    '''
    test_upvote_when_user_change_vote_from_upvote_to_None
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=True, user=user, answer=answer)

    vote = avote.save_vote(True)
    assert vote == None
    assert avote.vote == None


@pytest.mark.django_db
def test_downvote_when_user_create_new_vote_for_downvote():
    '''
    test_downvote_when_user_create_new_vote_for_downvote
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(False)
    assert vote == False
    assert avote.vote == False


@pytest.mark.django_db
def test_downvote_when_user_change_vote_from_none_to_downvote():
    '''
    test_downvote_when_user_change_vote_from_none_to_downvote
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(False)
    assert vote == False
    assert avote.vote == False


@pytest.mark.django_db
def test_downvote_when_user_change_vote_from_upvote_to_downupvote():
    '''
    test_downvote_when_user_change_vote_from_upvote_to_downupvote
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(False)
    assert vote == False
    assert avote.vote == False


@pytest.mark.django_db
def test_downvote_when_user_change_vote_from_downvote_to_None():
    '''
    test_downvote_when_user_change_vote_from_downvote_to_None
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=False, user=user, answer=answer)

    vote = avote.save_vote(False)
    assert vote == None
    assert avote.vote == None


@pytest.mark.django_db
def test_count_upvote_when_user_create_new_vote_for_upvote():
    '''
    test_count_upvote_when_user_create_new_vote_for_upvote
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(True)
    count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
    assert count_upvote == 1

@pytest.mark.django_db
def test_count_upvote_when_user_change_vote_from_none_to_upvote():
    '''
    test_count_upvote_when_user_change_vote_from_none_to_upvote
    '''

    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(True)
    count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
    assert count_upvote == 1

@pytest.mark.django_db
def test_count_upvote_when_user_change_vote_from_downvote_to_upvote():
    '''
    test_count_upvote_when_user_change_vote_from_downvote_to_upvote
    '''

    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(True)
    count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
    assert count_upvote == 1



@pytest.mark.django_db
def test_count_upvote_when_user_change_vote_from_upvote_to_None	():
    '''
    test_count_upvote_when_user_change_vote_from_upvote_to_None
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=True, user=user, answer=answer)

    vote = avote.save_vote(True)
    count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
    assert count_upvote == 0



@pytest.mark.django_db
def test_count_downvote_when_user_create_new_vote_for_downvote():
    '''
    test_count_downvote_when_user_create_new_vote_for_downvote
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)
    vote = avote.save_vote(False)
    count_upvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    assert count_upvote == 1


@pytest.mark.django_db
def test_count_downvote_when_user_change_vote_from_none_to_downvote	():
    '''
    test_count_downvote_when_user_change_vote_from_none_to_downvote
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)
    vote = avote.save_vote(False)
    count_upvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    assert count_upvote == 1


@pytest.mark.django_db
def test_count_downvote_when_user_change_vote_from_upvote_to_downupvote():
    '''
    test_count_downvote_when_user_change_vote_from_upvote_to_downupvote
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=None, user=user, answer=answer)

    vote = avote.save_vote(False)
    count_upvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    assert count_upvote == 1


@pytest.mark.django_db
def test_count_downvote_when_user_change_vote_from_downvote_to_None():
    '''
    test_count_downvote_when_user_change_vote_from_downvote_to_None
    '''
    user = User(username='test', password='test', email='test@test.com')
    user.save()
    question = Question.objects.create(question_text="How can I fly over the mountain?", user=user, created_date=timezone.now())
    question.save()
    answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=question, user=user, created_date=timezone.now())
    answer.save()
    comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
    comment.save()
    avote = Voteanswer(vote=False, user=user, answer=answer)

    vote = avote.save_vote(False)
    count_upvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    assert count_upvote == 0



