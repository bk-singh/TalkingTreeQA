import pytest
from django.db import IntegrityError
from talkingtree.models import Question, Answer, Comment, Voteanswer, Votecomment
from django.contrib.auth.models import User
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
def test_search_no_matching_questions_count_to_zero(question, user):
    '''
    test_search_no_matching_questions_count_to_zero
    '''
    search_text = 'aaaaaaaaa'
    que = Question()
    questions = que.search(search_text=search_text)
    assert questions.count() == 0


@pytest.mark.django_db
def test_search_matching_questions_count_to_not_zero(question, user):
    '''
    test_search_matching_questions_count_to_not_zero
    '''
    search_text = 'How'
    que = Question()
    questions = que.search(search_text=search_text)
    assert isinstance(questions.first(), Question)
    assert questions.count() > 0


@pytest.mark.django_db
def test_create_a_question_with_valid_input_increase_question_count_by_one(question, user):
    '''
    test_search_matching_questions_count_to_not_zero
    '''
    question_count_before_creating_new_question = Question.objects.all().count()
    question = Question.objects.create(question_text="Is this new question?", user=user,
                                       created_date=timezone.now())
    question.save()
    question_count_after_creating_new_question = Question.objects.all().count()

    assert isinstance(question, Question)
    assert question_count_after_creating_new_question == question_count_before_creating_new_question + 1


@pytest.mark.django_db
def test_update_question_changes_question_text(question, user):
    '''
    test_update_question_changes_question_text
    '''
    question.question_text = "question after update?"
    question.save()
    question1 = Question.objects.get(pk=question.id)
    assert isinstance(question, Question)
    assert question1.question_text == question.question_text
    assert question1.question_text == "question after update?"


@pytest.mark.django_db
def test_delete_question_remove_an_existing_question_and_decreases_question_count_by_one(question, user):
    '''
    test_delete_an_existing_question
    '''
    count_question_before_delete = Question.objects.all().count()
    question.delete()
    assert Question.objects.all().count() == count_question_before_delete -1
    with pytest.raises(Question.DoesNotExist):
        question1 = Question.objects.get(pk=question.id)


@pytest.mark.django_db
def test_new_answer_missing_question_raises_integrity_error(question, user):
    '''
    test_new_answer_missing_question_raises_Integrity_Error
    '''
    with pytest.raises(IntegrityError):
        answer = Answer.objects.create(answer_text="You can use Parachute or Aeroplane.", question=None, user=user, created_date=timezone.now())
        answer.save()


@pytest.mark.django_db
def test_new_comment_missing_answer_raises_integrity_error(question, answer, user):
    '''
    test_new_comment_missing_answer_raises_Integrity_Error
    '''
    with pytest.raises(IntegrityError):
        comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=None, user=user,
                                         created_date=timezone.now())
        comment.save()


@pytest.mark.django_db
def test_upvote_for_new_upvote_increments_upvotes_count(question, answer, user):
    '''
    test_upvote_when_user_create_new_vote_for_upvote
    '''
    avote = Voteanswer(vote=None, user=user, answer=answer)
    vote = avote.save_vote(True)
    count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
    assert vote == True
    assert avote.vote == True
    assert count_upvote == 1

@pytest.mark.django_db
def test_upvote_for_triple_upvote_increments_upvotes_count(question, answer, user):
    '''
    test_upvote_when_user_change_vote_from_none_to_upvote
    '''
    avote = Voteanswer(vote=None, user=user, answer=answer)
    vote = avote.save_vote(True)
    vote = avote.save_vote(True)
    vote = avote.save_vote(True)
    count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()

    assert vote == True
    assert avote.vote == True
    assert count_upvote == 1


@pytest.mark.django_db
def test_upvote_for_upvote_after_downvote_increments_upvotes_count_and_decreament_downvote_count(question, answer, user):
    '''
    test_upvote_when_user_change_vote_from_downvote_to_upvote
    '''
    avote = Voteanswer(vote=None, user=user, answer=answer)
    vote = avote.save_vote(False)
    count_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()

    vote = avote.save_vote(True)
    count_upvote_after_upvoted = Voteanswer.objects.filter(vote=True, answer=answer).count()
    count_downvote_after_upvoted = Voteanswer.objects.filter(vote=False, answer=answer).count()

    assert vote == True
    assert avote.vote == True
    assert count_upvote + 1 == count_upvote_after_upvoted
    assert count_downvote - 1  == count_downvote_after_upvoted


@pytest.mark.django_db
def test_upvote_for_already_upvoted_answer_decrements_upvotes_count(question, answer, user):
    '''
    test_upvote_when_user_change_vote_from_upvote_to_None
    '''

    avote = Voteanswer(vote=None, user=user, answer=answer)
    vote = avote.save_vote(True)
    count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
    vote = avote.save_vote(True)
    count_upvote_after_upvoted = Voteanswer.objects.filter(vote=True, answer=answer).count()
    assert vote == None
    assert avote.vote == None
    assert count_upvote - 1 == count_upvote_after_upvoted


@pytest.mark.django_db
def test_downvote_for_new_downvote_increments_downvotes_count(question, answer, user):
    '''
    test_downvote_when_user_create_new_vote_for_downvote
    '''

    avote = Voteanswer(vote=None, user=user, answer=answer)
    count_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    vote = avote.save_vote(False)
    count_downvote_after_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()

    assert vote == False
    assert avote.vote == False
    assert count_downvote+1 ==count_downvote_after_downvote


@pytest.mark.django_db
def test_downvote_for_triple_downvote_increments_downvotes_count(question, answer, user):
    '''
    test_downvote_when_user_change_vote_from_none_to_downvote
    '''

    avote = Voteanswer(vote=None, user=user, answer=answer)
    count_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    vote = avote.save_vote(False)
    vote = avote.save_vote(False)
    vote = avote.save_vote(False)
    count_downvote_after_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    assert vote == False
    assert avote.vote == False
    assert count_downvote+1 == count_downvote_after_downvote


@pytest.mark.django_db
def test_downvote_for_downvote_an_upvoted_answer_increments_downvotes_count_and_decrements_count(question, answer, user):
    '''
    test_downvote_when_user_change_vote_from_upvote_to_downupvote
    '''

    avote = Voteanswer(vote=None, user=user, answer=answer)
    vote = avote.save_vote(True)
    count_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
    vote = avote.save_vote(False)
    count_downvote_after_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    count_upvote_after_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()

    assert vote == False
    assert avote.vote == False
    assert count_upvote-1 == count_upvote_after_upvote
    assert count_downvote+1 == count_downvote_after_downvote


@pytest.mark.django_db
def test_downvote_for_already_downvoted_answer_decrement_downvotes_count(question, answer, user):
    '''
    test_downvote_when_user_change_vote_from_downvote_to_None
    '''
    avote = Voteanswer(vote=None, user=user, answer=answer)
    vote = avote.save_vote(False)
    count_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    vote = avote.save_vote(False)
    count_downvote_after_downvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
    assert vote == None
    assert avote.vote == None
    assert count_downvote-1 == count_downvote_after_downvote
#
#
# @pytest.mark.django_db
# def test_count_upvote_when_user_create_new_vote_for_upvote(question, answer, user):
#     '''
#     test_count_upvote_when_user_create_new_vote_for_upvote
#     '''
#     comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
#     comment.save()
#     avote = Voteanswer(vote=None, user=user, answer=answer)
#
#     vote = avote.save_vote(True)
#     count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
#     assert count_upvote == 1
#
# @pytest.mark.django_db
# def test_count_upvote_when_user_change_vote_from_none_to_upvote(question, answer, user):
#     '''
#     test_count_upvote_when_user_change_vote_from_none_to_upvote
#     '''
#
#
#     comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
#     comment.save()
#     avote = Voteanswer(vote=None, user=user, answer=answer)
#
#     vote = avote.save_vote(True)
#     count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
#     assert count_upvote == 1
#
# @pytest.mark.django_db
# def test_count_upvote_when_user_change_vote_from_downvote_to_upvote(question, answer, user):
#     '''
#     test_count_upvote_when_user_change_vote_from_downvote_to_upvote
#     '''
#
#     comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
#     comment.save()
#     avote = Voteanswer(vote=None, user=user, answer=answer)
#
#     vote = avote.save_vote(True)
#     count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
#     assert count_upvote == 1
#
#
#
# @pytest.mark.django_db
# def test_count_upvote_when_user_change_vote_from_upvote_to_None	(question, answer, user):
#     '''
#     test_count_upvote_when_user_change_vote_from_upvote_to_None
#     '''
#
#     comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
#     comment.save()
#     avote = Voteanswer(vote=True, user=user, answer=answer)
#
#     vote = avote.save_vote(True)
#     count_upvote = Voteanswer.objects.filter(vote=True, answer=answer).count()
#     assert count_upvote == 0
#
#
#
# @pytest.mark.django_db
# def test_count_downvote_when_user_create_new_vote_for_downvote(question, answer, user):
#     '''
#     test_count_downvote_when_user_create_new_vote_for_downvote
#     '''
#
#     comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
#     comment.save()
#     avote = Voteanswer(vote=None, user=user, answer=answer)
#     vote = avote.save_vote(False)
#     count_upvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
#     assert count_upvote == 1
#
#
# @pytest.mark.django_db
# def test_count_downvote_when_user_change_vote_from_none_to_downvote	(question, answer, user):
#     '''
#     test_count_downvote_when_user_change_vote_from_none_to_downvote
#     '''
#
#     comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
#     comment.save()
#     avote = Voteanswer(vote=None, user=user, answer=answer)
#     vote = avote.save_vote(False)
#     count_upvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
#     assert count_upvote == 1
#
#
# @pytest.mark.django_db
# def test_count_downvote_when_user_change_vote_from_upvote_to_downupvote(question, answer, user):
#     '''
#     test_count_downvote_when_user_change_vote_from_upvote_to_downupvote
#     '''
#
#     comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
#     comment.save()
#     avote = Voteanswer(vote=None, user=user, answer=answer)
#
#     vote = avote.save_vote(False)
#     count_upvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
#     assert count_upvote == 1
#
#
# @pytest.mark.django_db
# def test_count_downvote_when_user_change_vote_from_downvote_to_None(question, answer, user):
#     '''
#     test_count_downvote_when_user_change_vote_from_downvote_to_None
#     '''
#
#     comment = Comment.objects.create(comment_text="I cannot by an Aeroplane. ", answer=answer, user=user, created_date=timezone.now())
#     comment.save()
#     avote = Voteanswer(vote=False, user=user, answer=answer)
#
#     vote = avote.save_vote(False)
#     count_upvote = Voteanswer.objects.filter(vote=False, answer=answer).count()
#     assert count_upvote == 0
#
#
#
