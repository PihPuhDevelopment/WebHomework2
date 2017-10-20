# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse
from askleo import settings

# Create your views here.


def printparams(request):
    response = ''
    if request.method == 'GET':
        response = ''.join('%s : %s\n' % (key, value) for key, value in request.GET.items());
    elif request.method == 'POST':
        response = ''.join('%s : %s\n' % (key, value) for key, value in request.POST.items());
    return HttpResponse(response)


def default(request):
    context = {'username': 'Mr. ButtFlame',
               'questiontitle': 'Java, JDBC, GROUP BY ROLLUP',
               'questionsnip': 'В 1С при обходе результата запроса можно обходить запрос иерархически. Каждый итоговый результат содержит кроме полей, еще и вложенный результат, который так же...'}
    response = render(request, 'question.html', context)
    response['Cache-Control'] = 'public must-revalidate max-age=60'
    return response

