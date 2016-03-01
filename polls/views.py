from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Question, Choice
from django.utils import timezone

# Create your views here.

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_questions_list'

	# defining latest_questions_list
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] # lte is <=. Filtering out future posts


# subclass DetailView as all it does is pull 1 variable or 404
class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	# override get_queryset method - (testing)
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())


# subclass DetailView as all it does is pull 1 variable or 404
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

	# override get_queryset method - (testing)
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	# trying to grab choice from form post var otherwise error
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		context = {
					'question':p, 
					'error_message': 'Please select a choice'
				}
		return render(request, 'polls/detail.html', context)
	else:
		# increasing vote count by 1 and sending user to votes page
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

		return render(request, 'polls/vote.html', {'question': question})