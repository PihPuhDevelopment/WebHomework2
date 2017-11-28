from django.core.management.base import BaseCommand, CommandError
from questions.models import Profile, Tag, Question, Answer, AnswerLike, QuestionLike
from faker import Faker
import json
import random

fake = Faker()
with open("/home/leonid/ParkMail/Web/askleo/askleo/questions/management/commands/langs.json", "r") as langs:
    tags = json.load(langs)

tags = tags["languages"]


class Command(BaseCommand):
    help = "Fills database with random users, questions, answers, tags and likes"

    def add_arguments(self, parser):
        parser.add_argument("--n_users", action="store", nargs=1, type=int, default=5)
        parser.add_argument("--n_questions", action="store", nargs=1, type=int, default=5)
        parser.add_argument("--n_answers", action="store", nargs=1, type=int, default=15)
        parser.add_argument("--n_qlikes", action="store", nargs=1, type=int, default=7)
        parser.add_argument("--n_alikes", action="store", nargs=1, type=int, default=20)
        parser.add_argument("--n_tags", action="store", nargs=1, type=int, default=20)

    def handle(self, *args, **options):
        for i in range(0, options["n_users"]):
            #generate some random users
            fake_profile = fake.simple_profile()
            profile = Profile(username=fake_profile["name"], email=fake_profile["mail"], login=fake_profile["username"], password=fake.password())
            profile.save()

        tags_indexes = list(range(0, len(tags)))
        random.shuffle(tags_indexes)
        for i in range(0, options["n_tags"]):
            #add random tags from file
            tag = Tag(name=tags[tags_indexes[i]])
            tag.save()

        for i in range(0, options["n_questions"]):
            #generate some random questoins
            question_text = fake.text(max_nb_chars=400)
            question_snippet = question_text[:97] + "..."
            question_title = fake.sentence()
            question_title = question_title[:(len(question_title)-1)] + "?"
            tag_objects = list(Tag.objects.all())
            random.shuffle(tag_objects)
            rand_user = Profile.objects.all()[random.randrange(0, len(Profile.objects.all())-1)]

            question = Question(text=question_text, snippet=question_snippet, title=question_title, user=rand_user)
            question.save()
            for i in range(0, random.randrange(2, 4)):
                question.tags.add(tag_objects[i])

            question.save()

        for i in range(0, options["n_answers"]):
            #generate some random answers
            answer_text = fake.text(max_nb_chars = 250)
            answer_user = Profile.objects.all()[random.randrange(0, len(Profile.objects.all())-1)]
            ans_question = Question.objects.all()[random.randrange(0, len(Question.objects.all())-1)]
            answer_correct = not random.getrandbits(1)
            answer = Answer(text=answer_text, user = answer_user,
                            question=ans_question, correct=answer_correct)
            answer.save()

        for i in range(0, options["n_qlikes"]):
            print
            qlike_question = Question.objects.all()[random.randrange(0, len(Question.objects.all())-1)]
            qlike_user = Profile.objects.all()[random.randrange(0, len(Profile.objects.all())-1)]
            while QuestionLike.objects.filter(questionLiked=qlike_question, user=qlike_user):
                qlike_question = Question.objects.all()[random.randrange(0, len(Question.objects.all())-1)]
                qlike_user = Profile.objects.all()[random.randrange(0, len(Profile.objects.all())-1)]
            print("success N" + str(i+1))
            like_or_dis = not random.getrandbits(1)
            qlike = QuestionLike(questionLiked=qlike_question, user=qlike_user, like_or_dis=like_or_dis)
            qlike.save()

        for i in range(0, options["n_alikes"]):
            alike_answer = Answer.objects.all()[random.randrange(0, len(Answer.objects.all())-1)]
            alike_user = Profile.objects.all()[random.randrange(0, len(Profile.objects.all())-1)]
            while AnswerLike.objects.filter(answerLiked=alike_answer, user=alike_user):
                alike_answer = Answer.objects.all()[random.randrange(0, len(Answer.objects.all())-1)]
                alike_user = Profile.objects.all()[random.randrange(0, len(Profile.objects.all())-1)]
            like_or_dis = not random.getrandbits(1)
            qlike = AnswerLike(answerLiked=alike_answer, user=alike_user, like_or_dis=like_or_dis)
            qlike.save()