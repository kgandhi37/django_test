# from __future__ import unicode_literals # for python3? read up

from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Question(models.Model):
	# in django, ID field is automatically added
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published') # name in administration

	# define string representation
	def __str__(self):
		return self.question_text

	#creating a custom method (for admin view)
	def was_published_in_last_7_days(self):
		now = timezone.now()
		return timezone.now() - datetime.timedelta(days=7) <= self.pub_date <= now # written this way to avoid questions that are not in the future AND < 7 days old

	# customising method column view
	was_published_in_last_7_days.admin_order_field = 'pub_date' # defining how to be sorted when clicking on label
	was_published_in_last_7_days.boolean = True 
	was_published_in_last_7_days.short_description = 'Published in the past week?' # column label


class Choice(models.Model):

	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	question = models.ForeignKey(Question) # note using class name here

	def __str__(self):
		return self.choice_text