from django.core.management.base import BaseCommand, CommandError
from questions.models import Profile, Tag, Question, Answer, AnswerLike, QuestionLike
from faker import Faker

fake = Faker()
tags = ['java', 'js', 'python', 'django', 'css', 'html', 'c++', 'c', 'SQL', 'MongoDB']

class Command(BaseCommand):
    help = "Fills database with random users, questions, answers, tags and likes"

    def add_arguments(self, parser):
        parser.add_argument("--n_users", action="store", nargs=1, type=int, default=2)
        parser.add_argument("--n_questions", action="store", nargs=1, type=int, default=5)
        parser.add_argument("--n_answers", action="store", nargs=1, type=int, default=15)
        parser.add_argument("--n_likes", action="store", nargs=1, type=int, default=35)

    def handle(self, *args, **options):
        for i in range(0, options["n_users"]):
            #generate some random users

            pass

        for i in range(0, options["n_tags"]):
            #generate some random tags
            pass

        for i in range(0, options["n_questions"]):
            #generate some random questoins
            pass

        for i in range(0, options["n_answers"]):
            #generate some random answers
            pass

        for i in range(0, options["n_likes"]):
            #generate some random likes to questions and answers
            pass