# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from askleo import settings
from django.core.paginator import Paginator
from models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike
import json

# Create your views here.
ITEMS_PER_PAGE = 7


#with open('/home/leonid/ParkMail/Web/askleo/askleo/static/data.json'.encode('utf-8'), 'r'.encode('utf-8')) as infile:
    #qs = json.load(infile)


def paginate(objects, request):
    if 'page' in request.GET:
        pagenum = int(request.GET['page'])
    else:
        pagenum = 1

    pages = Paginator(objects, ITEMS_PER_PAGE)
    obj_on_page = pages.page(pagenum).object_list
    return obj_on_page, pages, pagenum


def index(request):
    all_questions = Question.objects.with_rating();

    qs_on_page, pages, pagenum = paginate(all_questions, request)

    context = {'qs': qs_on_page, 'pagenum': range(1, pages.num_pages), 'current': pagenum}

    return render(request, 'index.html', context)


def hot_questions(request):
    hots = Question.objects.hot_questions()

    hots_on_page, pages, pagenum = paginate(hots, request)

    context = {'qs': hots_on_page, 'pagenum': range(1, pages.num_pages), 'current': pagenum}
    return render(request, 'hots.html', context)


def questions_by_tag(request, tag):
    tagged = Question.objects.filter_with_rating(tags__name=tag)

    tagged_on_page, pages, pagenum = paginate(tagged, request)

    context = {'qs': tagged_on_page, 'tag': tag, 'pagenum': range(1, pages.num_pages), 'current': pagenum}

    return render(request, 'tag.html', context)

def single_question(request, question_number):
    try:
        question = Question.objects.get_with_rating(id=int(question_number))
    except Question.DoesNotExist:
        return Http404()

    answers = Answer.objects.filter_with_rating(question_id=question.id)

    context = {'question': question, 'answers': answers}

    return render(request, 'question.html', context)


def signin(request):
    return render(request, 'login.html', {})


def signup(request):
    return render(request, 'register.html', {})


def ask(request):
    return render(request, 'ask.html', {})

