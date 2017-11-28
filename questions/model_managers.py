from django.db import models

class AnswerManager(models.Manager):

    def filter_with_rating(self, **kwargs):
        answers = self.model.objects.filter(**kwargs)
        for answer in answers:
            self.__add_rating(answer)
        return answers

    def __add_rating(self, answer):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT * from questions_answerlike WHERE answerLiked_id = %s",
                       (answer.id,))
        rating = 0
        for row in cursor.fetchall():
            if row[3]:
                rating += 1
            else:
                rating -= 1
        answer.rating = rating


class QuestionManager(models.Manager):
    def with_rating(self):
        questions = list(self.model.objects.all().order_by("-date"))
        for question in questions:
            self.__add_rating(question)
        return questions

    def get_with_rating(self, **kwargs):
        question = self.model.objects.get(**kwargs)
        self.__add_rating(question)
        return question

    def filter_with_rating(self, **kwargs):
        questions = list(self.model.objects.filter(**kwargs).order_by("-date"))
        for question in questions:
            self.__add_rating(question)
        return questions

    def hot_questions(self):
        questions = self.with_rating()
        questions.sort(key=lambda question: question.rating, reverse=True)
        return questions[:10]

    def __add_rating(self, question):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT * from questions_questionlike as ql WHERE questionLiked_id = %s",
                       (question.id,))
        rating = 0
        for row in cursor.fetchall():
            if row[3]:
                rating += 1
            else:
                rating -= 1
        question.rating = rating



