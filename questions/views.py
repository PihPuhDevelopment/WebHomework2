# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import Http404, JsonResponse
# django imports
from django.shortcuts import render, redirect

from models import Profile, Question, Answer
# my imports
from questions.forms import RegisterForm, LoginForm, AuthorForm, AnswerForm, ProfileForm, AskForm

ITEMS_PER_PAGE = 7
PAGES_PER_PAGE = 10


def add_user(request, context):
    _profile = Profile.objects.filter(user_ptr_id=request.user.id).last()
    context['userinfo'] = _profile
    return context


def paginate(objects, request):
    if 'page' in request.GET:
        pagenum = int(request.GET['page'])
    else:
        pagenum = 1

    pages = Paginator(objects, ITEMS_PER_PAGE)
    obj_on_page = pages.page(pagenum).object_list
    return obj_on_page, pages, pagenum


def index(request):
    all_questions = Question.objects.with_rating()

    qs_on_page, pages, pagenum = paginate(all_questions, request)

    first_page = pagenum - PAGES_PER_PAGE / 2
    if first_page <= 0:
        first_page = 1
    else:
        first_page = int(first_page)

    last_page = first_page + PAGES_PER_PAGE
    if last_page > pages.num_pages:
        last_page = pages.num_pages

    print(first_page)
    print(last_page)

    context = {'qs': qs_on_page,
               'pagenum': range(first_page, last_page),
               'current': pagenum,
               'userinfo': profile}

    context = add_user(request, context)

    return render(request, 'index.html', context)


def hot_questions(request):
    hots = Question.objects.hot_questions()

    hots_on_page, pages, pagenum = paginate(hots, request)

    context = {'qs': hots_on_page,
               'pagenum': range(1, pages.num_pages),
               'current': pagenum}
    context = add_user(request, context)
    return render(request, 'hots.html', context)


def questions_by_tag(request, tag):
    tagged = Question.objects.filter_with_rating(tags__name=tag)

    tagged_on_page, pages, pagenum = paginate(tagged, request)

    context = {'qs': tagged_on_page, 'tag': tag, 'pagenum': range(1, pages.num_pages), 'current': pagenum}
    context = add_user(request, context)
    return render(request, 'tag.html', context)


def single_question(request, question_number):

    try:
        question = Question.objects.get_with_rating(id=int(question_number))
    except Question.DoesNotExist:
        return Http404()

    answers = Answer.objects.filter_with_rating(question_id=question.id)

    context = {'question': question, 'answers': answers}
    context = add_user(request, context)

    if request.method == 'POST':
        form = AnswerForm(request.POST, context["userinfo"], question)
        if form.is_valid():
            form.save()
            return redirect('question', question_number)
    else:
        form = AnswerForm()

    context['form'] = form

    return render(request, 'question.html', context)


def signin(request):
    if request.user.is_authenticated:
        context = {}
        context = add_user(request, context)
        return render(request, 'already_signed_in.html', context)
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, "Username or password is incorrect")

    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        context = {}
        context = add_user(request, context)
        return render(request, 'already_signed_in.html', context)
    if request.method == 'GET':
        register_form = RegisterForm()
    else:
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return redirect('index')
    return render(request, 'register.html', {'form': register_form})


@login_required
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST, Profile.objects.get(id=request.user.id))
        if form.is_valid():
            new_question = form.save()
            return redirect('question', new_question.id)
    else:
        form = AskForm()

    context = {'form': form}
    context = add_user(request, context)
    return render(request, 'ask.html', context)


def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            return redirect("/")
    else:
        form = AuthorForm()

    context = {'form': form}
    context = add_user(request, context)
    return render(request, "form.html", context)


def create_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            return redirect("/")
    else:
        form = AnswerForm()

    context = {'form': form}
    context = add_user(request, context)
    return render(request, "form.html", context)


@login_required()
def log_out(request):
    logout(request)
    return redirect("/")


@login_required()
def profile(request):
    user = request.user
    _profile = Profile.objects.filter(user_ptr_id=user.id).last()
    print(_profile)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES)
        print("is post")
        if form.is_valid():
            print("valid")
            _profile.avatar = form.cleaned_data["avatar"]
            _profile.save()

    context = {}
    context = add_user(request, context)
    return render(request, 'profile.html', context)


@login_required()
def vote(request):
    try:
        qid = int(request.POST.get('qid'))
    except:
        return JsonResponse(dict(error='bad question id'))
    _vote = request.POST.get('vote')
    question = Question.objects.get_with_rating(id=qid)
    rating = question.rating
    if _vote == "inc":
        rating += 1
    else:
        rating -= 1
    return JsonResponse(dict(ok=1, vote=_vote, rating=rating))
