# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse
from askleo import settings
from django.core.paginator import Paginator
import json

# Create your views here.
ITEMS_PER_PAGE = 7


with open('/home/leonid/ParkMail/Web/askleo/askleo/static/data.json'.encode('utf-8'), 'r'.encode('utf-8')) as infile:
    qs = json.load(infile)


def paginate(objects, request):
    if 'page' in request.GET:
        pagenum = int(request.GET['page'])
    else:
        pagenum = 1

    pages = Paginator(objects, ITEMS_PER_PAGE)
    obj_on_page = pages.page(pagenum).object_list
    return obj_on_page, pages, pagenum


def index(request):
    qs_on_page, pages, pagenum = paginate(qs, request)

    context = {'qs': qs_on_page, 'pagenum': range(1, pages.num_pages), 'current': pagenum}

    response = render(request, 'index.html', context)
    return response


def hot_questions(request, hot_page):
    hots = []
    for q in qs:
        if q['likes'] > 200:
            hots.append(q)

    hots_on_page = paginate(hots, request)

    context = {'qs': hots_on_page}
    response = render(request, 'hots.html', context)
    return response


def questions_by_tag(request, tag):
    tagged = []
    for q in qs:
        if tag in q['tags']:
            tagged.append(q)

    tagged_on_page = paginate(tagged, request)

    context = {'qs': tagged_on_page, 'tag': tag}
    response = render(request, 'tag.html', context)
    return response

def single_question(request, question_number):
    qnum = int(question_number)
    context = {'question': qs[qnum-1]}
    response = render(request, 'question.html', context)
    return response


def signin(request):
    return render(request, 'login.html', {})


def signup(request):
    return render(request, 'register.html', {})


def ask(request):
    return render(request, 'ask.html', {})

