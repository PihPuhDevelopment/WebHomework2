# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from questions.exceptions import CorrectAlreadyExists
from model_managers import QuestionManager, AnswerManager

# Create your models here.


class Profile(User):
    login = models.CharField(max_length=30, verbose_name="login used to enter site")
    avatar = models.ImageField(upload_to='images/', null=True, verbose_name="user photo")


class Tag(models.Model):
    name = models.CharField(max_length=40, verbose_name="tag's title")


class Question(models.Model):
    text = models.TextField(verbose_name="question text")
    snippet = models.CharField(max_length=100, verbose_name="shortened text displayed in questions list")
    title = models.CharField(max_length=100, verbose_name="question title")
    tags = models.ManyToManyField(Tag, verbose_name="list of tags")
    user = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, verbose_name="user reference")
    date = models.DateTimeField(auto_now=True, verbose_name="date when question was created")

    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField(verbose_name="answer text")
    user = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, verbose_name="user reference")
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, verbose_name="question reference")
    correct = models.BooleanField(default=False, verbose_name="shows if the answer is marked as correct")
    date = models.DateTimeField(auto_now=True, verbose_name="date when answer was created")

    objects = AnswerManager()

    def save(self, force_insert=False, force_update=False, **kwargs):
        if self.correct:
            try:
                other_answer = Answer.objects.get(question=self.question, correct=True)
            except Answer.DoesNotExist:
                super(Answer, self).save(force_insert, force_update)
            else:
                other_answer.correct = False;
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



