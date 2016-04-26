
"""from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Question

def index(request):
 latest_question_list = Question.objects.order_by('-pub_date')[:5]
 template = loader.get_template('polls/index.html')
 context = {
 'latest_question_list': latest_question_list,
}
 return HttpResponse(template.render(context, request))"""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Choice, Question
from django.views import generic
from django.utils import timezone 

class IndexView(generic.ListView):
 template_name = 'polls/index.html'
 context_object_name = 'latest_question_list'
 """def get_queryset(self):
  return Question.objects.order_by('-pub_date')[:5]"""
  
 def get_queryset(self):
  return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
 
"""class DetailView(generic.DetailView):
 model = Question
 template_name = 'polls/detail.html'
 
class ResultsView(generic.DetailView):
 model = Question
 template_name = 'polls/results.html' """




def index(request):
 latest_question_list = Question.objects.order_by('-pub_date')[:5]
 context = {'latest_question_list': latest_question_list}
 return render(request, 'polls/index.html', context)


#def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
#return HttpResponse("You're looking at question %s." % question_id)
 question = get_object_or_404(Question, pk=question_id)
 return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
 #response = "You're looking at the results of question %s.
 #return HttpResponse(response % question_id) 
 question = get_object_or_404(Question, pk=question_id)
 return render(request, 'polls/results.html', {'question': question})
 
#def vote(request, question_id):
#return HttpResponse("You're voting on question %s." % question_id)  
 

# ...
def vote(request, question_id):
 question = get_object_or_404(Question, pk=question_id)
 try:
  selected_choice = question.choice_set.get(pk=request.POST['choice'])
 except (KeyError, Choice.DoesNotExist):

  return render(request, 'polls/detail.html', {'question': question,'error_message': "You didn't select a choice.",})
 else:
  selected_choice.votes += 1
  selected_choice.save()
  return HttpResponseRedirect(reverse('poll_proj_django:results', args=(question.id,)))