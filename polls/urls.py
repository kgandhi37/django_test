from django.conf.urls import url
from . import views


# if url is /polls/ direct to index in controller for polls
urlpatterns = [	
				# leveraging Djangos generic views
				url(r'^$', views.IndexView.as_view(), name='index'), 
				url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'), 
				url(r'^(?P<pk>[0-9]+)/results$', views.ResultsView.as_view(), name='results'),
				# note above using pk as generic views expect them
				# below still using question_id as vote requires custom logic so is a non-generic view
				url(r'^(?P<question_id>[0-9]+)/vote$', views.vote, name='vote'),
			]