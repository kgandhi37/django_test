from django.test import TestCase
from .models import Question
from django.utils import timezone
import datetime

# to resolve urls 
from django.core.urlresolvers import reverse
# Create your tests here.

class QuestionMethodTests(TestCase):

	# testing method in Question Model

	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_in_last_7_days(), False) 

	def test_was_published_recently_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_in_last_7_days(), True)

# creating a question for testing
def create_question(question_text, days):
	# days = number of days offset from now (negative for past, positive for yet to be published)
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
	# checking if response is what we expect if no questions
	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200) # check status code
		self.assertContains(response, "You haven't uploaded any questions yet") # check returning correct string for no questions yet
		self.assertQuerysetEqual(response.context["latest_questions_list"], []) # check if latest_question_list var is empty

	def test_index_view_with_past_question(self):
		# should be displayed on index view
		create_question(question_text="Past Question", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_questions_list'],
			['<Question: Past Question>']
		)

	def test_index_view_with_future_question(self):
		# shouldn't be displayed on index view
		create_question(question_text="Future Question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "You haven't uploaded any questions yet", status_code=200) # check returning correct string for no questions yet
		self.assertQuerysetEqual(response.context["latest_questions_list"], [])

	def test_index_view_with_future_and_past_question(self):
		# only past question should be displayed
		create_question(question_text="Past Question", days=-30)
		create_question(question_text="Future Question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_questions_list'],
			['<Question: Past Question>']
		)

	def test_index_view_with_2_past_questions(self):
		create_question(question_text="Past Question", days=-30)
		create_question(question_text="Second Past Question", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_questions_list'],
			['<Question: Second Past Question>', '<Question: Past Question>']
		)

class QuestionIndexDetailTests(TestCase):

	def test_detail_view_with_a_past_question(self):
		past_question = create_question(question_text="Past Question", days=-5)
		response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
		self.assertContains(response, past_question.question_text, status_code=200)
