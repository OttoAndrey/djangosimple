from django.db.models import F
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'mysite/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).exclude(choice=None).order_by('-pub_date')[:5]


def testpage(request):
    return HttpResponse("tetstpage is here")


class DetailView(generic.DetailView):
    model = Question
    template_name = 'mysite/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).exclude(choice=None)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'mysite/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).exclude(choice=None)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Вот этот ['choice'] это атрибут name="" в шаблоне detail
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Снова показываем форму с вопросом и выборами ответов
        return render(request, 'mysite/detail.html', {'question': question, 'error_message': "Вариант ответа выбери, э!"})
    else:
        # Добавил F(), чтобы избежать race conditions
        selected_choice.votes = F('votes') + 1
        return HttpResponseRedirect(reverse('mysite:results', args=(question_id,)))
