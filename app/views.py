from django.contrib import auth
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from app.models import *
from app.forms import *

QUESTIONS_ON_PAGE = 20
ANSWERS_ON_PAGE = 5


def get_continued(request):
    return request.GET.get('continued', '')


def get_pagination_queryset(objects, count_obj, page_num):
    paginator = Paginator(objects, count_obj)
    return paginator.get_page(page_num)


# Create your views here.
def index(request):
    questions = get_pagination_queryset(Question.objects.get_new_questions(), QUESTIONS_ON_PAGE,
                                        request.GET.get('page'))
    best_tags = Tag.objects.get_popular_tags()[:10]
    best_users = Profile.objects.get_best_users()[:10]
    return render(request, 'index.html', {'page_obj': questions, 'best_tags': best_tags, 'best_users': best_users})


def question(request, id):
    question_obj = Question.objects.filter(pk=id).first()
    print(str(question_obj.date_publish))
    answers = get_pagination_queryset(question_obj.answers.order_by('-date_publish'), ANSWERS_ON_PAGE,
                                      request.GET.get('page'))
    if request.method == 'GET':
        pass
    return render(request, 'question.html', {'question': question_obj, 'page_obj': answers})


@login_required(login_url='/login')
def ask(request):
    if request.method == 'GET':
        form = AskForm()
        return render(request, 'ask.html', {'form': form})
    elif request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            author = Profile.objects.filter(user__username=request.user.username).first()
            q = Question(title=form.cleaned_data['title'], text=form.cleaned_data['text'], author=author)
            q.save()
            for tag in form.cleaned_data['tags'].split(','):
                tag_in_db = Tag.objects.filter(title=tag.rstrip().lstrip()).first()
                if tag_in_db is None:
                    tag_in_db = Tag(title=tag.rstrip().lstrip())
                    tag_in_db.save()
                q.tags.add(tag_in_db)
                q.save()

            return redirect(reverse('question', args=[q.id]))
        else:
            return render(request, 'ask.html', {'form': form})


def sign_up(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'signup.html', {'form': form})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = Profile.objects.create_user(form.cleaned_data['email'], form.cleaned_data['password'],
                                               form.cleaned_data['username'], form.cleaned_data['avatar'])
            user.save()
            user = auth.authenticate(**form.cleaned_data)
            auth.login(request, user)
            return redirect(reverse('index'))
        else:
            return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                try:
                    return redirect(get_continued(request))
                except Exception as e:
                    return redirect(reverse('index'))
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect(get_continued(request))


def hot(request):
    questions = get_pagination_queryset(Question.objects.get_best_questions(), QUESTIONS_ON_PAGE,
                                        request.GET.get('page'))
    return render(request, 'best_questions.html', {'page_obj': questions})


def tag(request, title):
    tag_ = Tag.objects.filter(title=title).first()

    questions = get_pagination_queryset(tag_.questions.all(), QUESTIONS_ON_PAGE, request.GET.get('page'))
    return render(request, 'tag.html', {'tag': tag_, 'page_obj': questions})


@login_required
def edit_profile(request):
    if request.method == 'GET':
        profile = Profile.objects.filter(user__username=request.user.username).first()
        data = {'username': profile.user.username, 'email': profile.user.email, 'avatar': profile.avatar}
        form = EditProfileForm(data=data)
        return render(request, 'edit_profile.html', {'form': form})
    elif request.method == 'POST':
        print(request.POST)
        form = EditProfileForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.filter(user__username=request.user.username).first()
            if form.cleaned_data['username'] != request.user.username and Profile.objects.filter(user__username=form.cleaned_data['username']).first() is not None:
                form.add_error('username', 'Such username is already exist')
                print('error!')
                return render(request, 'edit_profile.html', {'form': form})
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            if form.cleaned_data['new_password']:
                request.user.set_password(form.cleaned_data['new_password'])
            if form.cleaned_data['avatar']:
                profile.avatar = form.cleaned_data['avatar']
                profile.save()
            request.user.save()
            data = {'username': request.user.username, 'email': request.user.email, 'avatar': profile.avatar}
            form = EditProfileForm(data=data)
            return render(request, 'edit_profile.html', {'form': form})
        else:
            return render(request, 'signup.html', {'form': form})
