from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import *


# Create your views here.
def index(request):
    paginator = Paginator(Question.objects.get_new_questions(), 2)

    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': questions})


def question(request, id):
    question = Question.objects.filter(pk=id).first()
    paginator = Paginator(question.answers.all(), 2)

    page_number = request.GET.get('page')
    answers = paginator.get_page(page_number)

    return render(request, 'question.html', {'question': question, 'page_obj': answers})


def ask(request):
    return render(request, 'ask.html', {})


def sign_up(request):
    return render(request, 'signup.html', {})


def login(request):
    return render(request, 'login.html', {})


def hot(request):
    paginator = Paginator(Question.objects.get_best_questions(), 2)

    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)
    return render(request, 'best_questions.html', {'page_obj': questions})


def tag(request, title):
    tag_ = Tag.objects.filter(title=title).first()
    paginator = Paginator(tag_.questions.all(), 2)

    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)
    return render(request, 'tag.html', {'tag': tag_, 'page_obj': questions})
