from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Question


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'mysite/index.html', context)


def testpage(request):
    return HttpResponse("tetstpage is here")


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'mysite/detail.html', {'question': question})


def results(request, question_id):
    response = f'Ты смотришь на результаты опроса {question_id}'
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse(f'Ты отвечаешь на опрос {question_id}')