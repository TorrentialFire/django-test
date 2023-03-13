from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.views import generic

from .models import Choice, Question

# Create your views here.

# Generic/Class-based views docs: https://docs.djangoproject.com/en/4.1/topics/class-based-views/
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

#def index(request):    
    # Non-generic
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #context = {
    #    'latest_question_list': latest_question_list,
    #}
    #return render(request, 'polls/index.html', context)
    
    # Placeholder
    #return HttpResponse("Hello, world. You're at the polls index.")

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

#def detail(request, question_id):
    # Non-generic without shortcut
    #try:
    #    question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question does not exist")
    
    # Non-generic with shortcut
    #question = get_object_or_404(Question, pk=question_id)
    #return render(request, 'polls/detail.html', {'question': question})
    
    # Placeholder
    #return HttpResponse("You're looking at question {}.".format(question_id))

class ResultsView(generic.DeleteView):
    model = Question
    template_name = 'polls/results.html'

#def results(request, question_id):
    # Non-generic
    #question = get_object_or_404(Question, pk=question_id)
    #return render(request, 'polls/results.html', {'question': question})

    # Placeholder
    #return HttpResponse("You're looking at the results of question {}.".format(question_id))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Bad, python way of updating
        #select_choice.votes += 1
        #select_choice.save()

        # Good, database way of updating
        select_choice.votes = F('votes') + 1
        select_choice.save()
        
        # If you want to continue working with the object, refresh it from the database
        #select_choice.refresh_from_db()
         
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    #return HttpResponse("You're voting on question {}.".format(question_id))
