from django.core.management.base import BaseCommand
from app.models import *
from faker import Faker
from random import randint, choice
from mimesis import Generic, Text, Person, Datetime
from django.db.utils import IntegrityError


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.COUNT_USERS = 15000
        self.COUNT_TAGS = 12000
        self.COUNT_MAX_TAGS = 10
        self.COUNT_QUESTIONS = 150000
        self.COUNT_ANSWERS = 1500000
        self.COUNT_QUESTION_LIKES = 1500000
        self.COUNT_ANSWER_LIKES = 1500000
        # self.COUNT_USERS = 100
        # self.COUNT_TAGS = 1000
        # self.COUNT_MAX_TAGS = 10
        # self.COUNT_QUESTIONS = 1000
        # self.COUNT_ANSWERS = 1000
        # self.COUNT_QUESTION_LIKES = 5000
        # self.COUNT_ANSWER_LIKES = 5000
        self.users = []
        self.questions = []
        self.answers = []
        self.tags = []
        self.question_likes = []
        self.answers_likes = []

    def handle(self, *args, **options):
        self.create_users()
        print('users created')
        Profile.objects.bulk_create(self.users)
        print('users save')

        self.create_tags()
        print('tags created')
        Tag.objects.bulk_create(self.tags)
        print('tags save')

        self.create_questions()
        print('questions created')
        Question.objects.bulk_create(self.questions)
        print('questions save')
        self.create_tags_for_questions()
        print('questions tags added')

        self.create_answers()
        print('answers created')
        Answer.objects.bulk_create(self.answers)
        print('answers save')

        self.create_question_likes()
        print('like questions created')
        LikeQuestion.objects.bulk_create(self.question_likes)
        print('like questions save')

        self.create_answer_likes()
        print('like answers created')
        LikeAnswer.objects.bulk_create(self.answers_likes)
        print('like answers save')

    def create_users(self):
        text = Text()
        logins = text.words(quantity=self.COUNT_USERS)
        person = Person()
        for i in range(self.COUNT_USERS):
            # email = self.fake.unique.email()
            # name = self.fake.name()
            # login = self.fake.unique.word()
            try:
                email = person.email(unique=True)
                name = person.full_name()
                login = logins[i]
                self.users.append(Profile.objects.create_user(email, name, login, len(self.users) + 1))
                if i % 500 == 0:
                    print('users', i)
            except IntegrityError as e:
                continue

    def create_tags(self):
        text = Text()
        titles = list(set(text.words(quantity=self.COUNT_TAGS)))
        for i in range(len(titles)):
            try:
                self.tags.append(Tag(title=titles[i], id=len(self.tags) + 1))
                if i % 500 == 0:
                    print('tags', i)
            except IntegrityError as e:
                continue

    def create_questions(self):
        text_gen = Text()
        datet = Datetime()
        for i in range(self.COUNT_QUESTIONS):
            q_text = text_gen.text(quantity=randint(1, 30))
            q_title = text_gen.text(quantity=randint(1, 3))
            self.questions.append(self.create_question(
                title=q_title,
                text=q_text,
                author=self.get_random_user(),
                id=len(self.questions) + 1,
                date=datet.datetime(start=2007, end=2021)
            ))

    def create_tags_for_questions(self):
        for i in range(len(self.questions)):
            through_obj = []
            for j in range(randint(1, self.COUNT_MAX_TAGS)):
                through_obj.append(Question.tags.through(question_id=self.questions[i].id, tag_id=self.get_random_tag().id))
            try:
                Question.tags.through.objects.bulk_create(through_obj)
            except IntegrityError:
                pass
            if i % 1000 == 0:
                print('questions tag add', i)

    def create_answers(self):
        text_gen = Text()
        datet = Datetime()
        for i in range(self.COUNT_ANSWERS):
            a_text = text_gen.text(quantity=randint(1, 30))
            self.answers.append(self.create_answer(a_text, self.get_random_user(),
                                                   self.get_random_question(), len(self.answers) + 1,
                                                   datet.datetime(start=2007, end=2021)))
            if i % 5000 == 0:
                print('answers', i)

    def create_question_likes(self):
        for i in range(self.COUNT_QUESTION_LIKES):
            like_or_dislike = randint(1, 2)
            if like_or_dislike == 1:
                self.question_likes.append(
                    self.like_question(self.get_random_question(), self.get_random_user(), len(self.question_likes) + 1))
            else:
                self.question_likes.append(
                    self.dislike_question(self.get_random_question(), self.get_random_user(), len(self.question_likes) + 1))
            if i % 10000 == 0:
                print('question likes', i)

    def create_answer_likes(self):
        for i in range(self.COUNT_ANSWER_LIKES):
            like_or_dislike = randint(1, 2)
            if like_or_dislike == 1:
                self.answers_likes.append(self.like_answer(self.get_random_answer(), self.get_random_user(), len(self.answers_likes) + 1))
            else:
                self.answers_likes.append(
                    self.dislike_answer(self.get_random_answer(), self.get_random_user(), len(self.answers_likes) + 1))

            if i % 10000 == 0:
                print('answer likes', i)

    def get_random_user(self):
        return choice(self.users)

    def get_random_question(self):
        return choice(self.questions)

    def get_random_answer(self):
        return choice(self.answers)

    def get_random_tag(self):
        return choice(self.tags)

    def create_question(self, title, text, author, id, date):
        question = Question(title=title, text=text, author=author, id=id, date_publish=date)

        return question

    def create_answer(self, text, author, question, id, date):
        answer = Answer(text=text, author=author, question=question, id=id, date_publish=date)

        return answer

    def like_question(self, question, user, id):
        like = LikeQuestion(like_or_dislike=LikeQuestion.LIKE, question=question, user=user, id=id)

        return like

    def dislike_question(self, question, user, id):
        like = LikeQuestion(like_or_dislike=LikeQuestion.DISLIKE, question=question, user=user, id=id)

        return like

    def like_answer(self, answer, user, id):
        like = LikeAnswer(like_or_dislike=LikeAnswer.LIKE, answer=answer, user=user, id=id)

        return like

    def dislike_answer(self, answer, user, id):
        like = LikeAnswer(like_or_dislike=LikeAnswer.DISLIKE, answer=answer, user=user, id=id)

        return like
