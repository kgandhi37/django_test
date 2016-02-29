from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Question, Choice

# Create your views here.

def index(request):
	latest_questions_list = Question.objects.order_by('-pub_date')[:5] # order asc pub date, first 5 items
	context = {'latest_questions_list':latest_questions_list}
	return render(request, 'polls/index.html', context)

def detail(request, question_id): 
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	else: 
		return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	else:
		return render(request, 'polls/vote.html', {'question': question})