# -*- coding: utf-8 -*-
from django.conf import settings as s
from askleo import settings
import django
import sys
import os

sys.path.append('/home/leonid/ParkMail/Web/askleo/askleo')
#s.configure(settings, DEBUG=True)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askleo.settings')
django.setup()

from questions.models import Tag
from questions.models import Profile, Question
from faker import Faker
import random

fake = Faker()
tags = ['java', 'js', 'python', 'django', 'css', 'html', 'c++', 'c', 'SQL', 'MongoDB']

"""
for tname in tags:
    tag = Tag(name=tname)
    tag.save()
"""

"""
for i in range(0, 20):
    fProfile = fake.profile()
    profile = Profile(login=fProfile['username'], username=fProfile['name'], email=fProfile['mail'],
                      password=fake.password(length=10, special_chars=False, digits=True, upper_case=True,
                                             lower_case=True))
    profile.save()
"""

for i in range(0, 200):
    #генерация текста, названия, отрывка
    text = fake.text(max_nb_chars=200, ext_word_list=None)
    snippet = text[:97] + "..."
    title = fake.sentence(nb_words=random.randrange(5, 10))
    #генерация случайного пользователя, задавшего вопрос
    user_list = list(Profile.objects.all())
    random_user = user_list[random.randrange(0, len(user_list)-1)]
    #генерация трёх случайных тегов
    tag_list = list(Tag.objects.all())
    random_list = list(range(0, len(tag_list)))
    random.shuffle(random_list)
    tag1 = tag_list[random_list[0]]
    tag2 = tag_list[random_list[1]]
    tag3 = tag_list[random_list[2]]
    question = Question(text=text, snippet=snippet, title=title, user=random_user)
    question.save()
    question.tags.add(tag1)
    question.tags.add(tag2)
    question.tags.add(tag3)
    question.save()
    print(random_user.username)


for i in range(0, 500):
    text = fake.text(max_nb_chars=200, ext_word_list=None)
    user_list = list(Profile.objects.all())
    random_user = user_list[random.randrange(0, len(user_list) - 1)]
