from django.db import models


class QuestionManager(models.Manager):
    def with_rating(self):
        questions = list(self.model.objects.all().order_by("-date"))
        for question in questions:
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
        return questions

    def hot_questions(self):
        questions = self.with_rating()
        questions.sort(key=lambda question: question.rating, reverse=True)
        return questions[:10]

