from faker import Faker
import random
import json

fake = Faker()

questions = []
tags = ['java', 'js', 'python', 'django', 'css', 'html', 'c++', 'c', 'SQL', 'MongoDB']

for i in range(1, 50):
    content = fake.text(max_nb_chars=random.randrange(start=300, stop=600))
    snippet = content[:100] + "..."
    ts = fake.words(nb=3, ext_word_list=tags)
    questions.append(
        {
            'id': i,
            'title': fake.sentence(nb_words=8),
            'content': content,
            'snippet': snippet,
            'user_name': fake.name(),
            'likes': random.randrange(start=0, stop=250),
            'tags': ts,
            'answers': []
        }
    )
    num = random.randrange(start=0, stop=7)
    for j in range(1, num):
        q = questions[i-1]
        q['answers'].append(
            {
                'answer': fake.sentence(nb_words=random.randrange(start=5, stop=20)),
                'user_name': fake.name(),
                'likes': random.randrange(start=0, stop=15)
            }
        )


with open('data.json', 'w') as outfile:
    json.dump(questions, outfile)

