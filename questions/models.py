# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class AnswerManager(models.Manager):

    def filter_with_rating(self, **kwargs):
        answers = self.model.objects.filter(**kwargs)
        for answer in answers:
            self.__add_rating(answer)
        return answers

    def __add_rating(self, answer):
        likes = AnswerLike.objects.filter(answerLiked=answer)
        rating = 0
        for like in likes:
            if like.like_or_dis:
                rating += 1
            else:
                rating -= 1
        answer.rating = rating


class QuestionManager(models.Manager):
    def with_rating(self):
        questions = list(self.model.objects.all().order_by("-date"))
        for question in questions:
            self.__add_rating(question)
            self.__add_answer_count(question)
        return questions

    def get_with_rating(self, **kwargs):
        question = self.model.objects.get(**kwargs)
        self.__add_rating(question)
        self.__add_answer_count(question)
        return question

    def filter_with_rating(self, **kwargs):
        questions = list(self.model.objects.filter(**kwargs).order_by("-date"))
        for question in questions:
            self.__add_rating(question)
            self.__add_answer_count(question)
        return questions

    def hot_questions(self):
        questions = self.with_rating()
        questions.sort(key=lambda question: question.rating, reverse=True)
        return questions[:10]

    def __add_rating(self, question):
        likes = QuestionLike.objects.filter(questionLiked=question)
        rating = 0
        for like in likes:
            if like.like_or_dis:
                rating += 1
            else:
                rating -= 1
        question.rating = rating

    def __add_answer_count(self, question):
        answer_count = len(Answer.objects.filter(question=question))
        question.answer_count = answer_count


class Profile(User):
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', default="uploads/avatar.jpg", null=True, verbose_name="user photo")


class Tag(models.Model):
    name = models.CharField(max_length=40, verbose_name="tag's title", unique=True)


class Question(models.Model):
    text = models.TextField(verbose_name="question text")
    snippet = models.CharField(max_length=100, verbose_name="shortened text displayed in questions list")
    title = models.CharField(max_length=100, verbose_name="question title")
    tags = models.ManyToManyField(Tag, verbose_name="list of tags")
    user = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, verbose_name="user reference")
    date = models.DateTimeField(auto_now=True, verbose_name="date when question was created")

    objects = QuestionManager()

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField(verbose_name="answer text")
    user = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, verbose_name="user reference")
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, verbose_name="question reference")
    correct = models.BooleanField(default=False, verbose_name="shows if the answer is marked as correct")
    date = models.DateTimeField(auto_now=True, verbose_name="date when answer was created")

    objects = AnswerManager()

    def __unicode__(self):
        return str(self.text)[:20] + str(self.date)

    def save(self, force_insert=False, force_update=False, **kwargs):
        if self.correct:
            try:
                other_answer = Answer.objects.get(question=self.question, correct=True)
            except Answer.DoesNotExist:
                super(Answer, self).save(force_insert, force_update)
            else:
                other_answer.correct = False
                other_answer.save()
                super(Answer, self).save(force_insert, force_update)
        else:
            super(Answer, self).save(force_insert, force_update)


class AnswerLike(models.Model):
    answerLiked = models.ForeignKey(Answer, verbose_name="answer to which a like is related to")
    like_or_dis = models.BooleanField(verbose_name="shows if it is like or dislike (true-like, false-dislke)")
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="user reference")

    class Meta:
        unique_together = ("answerLiked", "user")


class QuestionLike(models.Model):
    questionLiked = models.ForeignKey(Question, verbose_name="question to which a like is related to")
    like_or_dis = models.BooleanField(verbose_name="shows if it is like or dislike (true-like, false-dislke)")
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="user reference")

    class Meta:
        unique_together = ("questionLiked", "user")