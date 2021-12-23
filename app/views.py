from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import *

QUESTIONS_ON_PAGE = 20
ANSWERS_ON_PAGE = 5


def get_pagination_queryset(objects, count_obj, page_num):
    paginator = Paginator(objects, count_obj)
    return paginator.get_page(page_num)


# Create your views here.
def index(request):
    questions = get_pagination_queryset(Question.objects.get_new_questions(), QUESTIONS_ON_PAGE, request.GET.get('page'))
    best_tags = Tag.objects.get_popular_tags()[:10]
    best_users = Profile.objects.get_best_users()[:10]
    return render(request, 'index.html', {'page_obj': questions, 'best_tags': best_tags, 'best_users': best_users})


def question(request, id):
    question_obj = Question.objects.filter(pk=id).first()
    print(str(question_obj.date_publish))
    answers = get_pagination_queryset(question_obj.answers.order_by('-date_publish'), ANSWERS_ON_PAGE, request.GET.get('page'))
    return render(request, 'question.html', {'question': question_obj, 'page_obj': answers})


def ask(request):
    return render(request, 'ask.html', {})


def sign_up(request):
    return render(request, 'signup.html', {})


def login(request):
    return render(request, 'login.html', {})


def hot(request):
    questions = get_pagination_queryset(Question.objects.get_best_questions(), QUESTIONS_ON_PAGE, request.GET.get('page'))
    return render(request, 'best_questions.html', {'page_obj': questions})


def tag(request, title):
    tag_ = Tag.objects.filter(title=title).first()

    questions = get_pagination_queryset(tag_.questions.all(), QUESTIONS_ON_PAGE, request.GET.get('page'))
    return render(request, 'tag.html', {'tag': tag_, 'page_obj': questions})
