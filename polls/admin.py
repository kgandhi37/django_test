from django.contrib import admin
# import our models
from .models import Question, Choice


#custom Admin Models

class ChoiceInline(admin.StackedInline):
	extra = 3 # default num of objects to add in model
	model = Choice

class QuestionAdmin(admin.ModelAdmin):
	# defining fieldsets
	fieldsets = [
		(None, {'fields' : ['question_text']}), 
		('Date Information', {'fields': ['pub_date']})
		]
	inlines = [ChoiceInline] 
	# displaying in Admin View. was_published is defined in the models.py file
	list_display = ('question_text', 'pub_date', 'was_published_in_last_7_days')
	# allow admins to filter by published date
	list_filter = ['pub_date']
	# allow admins to search questions
	search_fields = ['question_text']



# Registering models
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
