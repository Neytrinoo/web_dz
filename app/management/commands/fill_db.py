from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        # user = Profile.objects.create_user('aboba1@aboba.ru', 'abobich', 'ab0ba$$', None)
        # user.save()
        user1 = Profile.objects.create_user('user1@user.ru', 'user1', 'Ivanoff')
        user1.save()
        user2 = Profile.objects.create_user('user2@user.ru', 'user2', 'Petroff')
        user2.save()
        user3 = Profile.objects.create_user('user3@user.ru', 'user3', 'Жилда Былда')
        user3.save()
        user4 = Profile.objects.create_user('user4@user.ru', 'user4', 'Пупки')
        user4.save()

        tag1 = Tag(title='python')
        tag2 = Tag(title='django')
        tag3 = Tag(title='C++')
        tag4 = Tag(title='еда')
        tag5 = Tag(title='готовка')
        tag6 = Tag(title='животные')
        tag7 = Tag(title='arduino')
        tag8 = Tag(title='math')

        tag1.save()
        tag2.save()
        tag3.save()
        tag4.save()
        tag5.save()
        tag6.save()
        tag7.save()
        tag8.save()

        q1 = self.create_question(
            title='Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output - '
                  'while installing auto-py-to-exe through pip',
            text='I am trying to download auto-py-to-exe on a different (windows) device than I usually use through pip. '
                 'However when run I get the error (sorry it is so very very long). '
                 'Even though it does state that I need Visual Studio C++ 14.0 my computer won\'t install it and I have not needed it '
                 'before. I checked This Stack Overflow Question but it relates to another pip install and has no answers. If the only '
                 'answer is to install Visual Studio then I am kinda screwed.',
            author=user1
        )

        q1.tags.add(tag1)
        q1.tags.add(tag2)

        q2 = self.create_question(title='How can I convert an image to a 2d matrix?',
                                  text='I am Making a CNC machine that can print images(basically a printer). But I dont want any software '
                                       'where I can feed an image and it produces the g-code for me. I want to write my own code that will '
                                       'convert the image to 2d matrix which I can then feed to the motors through an arduino or some other '
                                       'microcontroller.',
                                  author=user2)
        q2.tags.add(tag3)
        q2.tags.add(tag7)

        q3 = self.create_question(title='Stacked Matplotlib Horizontal Bar Chart Python Not Showing all series',
                                  text='Essentially as of now only 4 of the 5 show up on the chart. When there should be 5 in total.',
                                  author=user2)

        q3.tags.add(tag1)
        q3.tags.add(tag8)


        q4 = self.create_question(title='TypeError: argument of type \'WindowsPath\' is not iterable',
                                  text='''I got the following error when running pytest:

>           needquote = (" " in arg) or ("\t" in arg) or not arg
E           TypeError: 'WindowsPath' object is not iterable
TypeError: argument of type 'WindowsPath' is not iterable
...\Miniconda3\envs\manubot-dev\lib\subprocess.py:461: TypeError
I fixed this by converting path to str:
Line 461: needquote = (" " in str(arg)) or ("\t" in str(arg)) or not str(arg)
Line 465: for c in str(arg):

.. according to this suggestion.

My programming background is pretty limited and I am not sure whether this solution fits for all, thus I am sharing it here (and not directly committing).''',
                                  author=user3)

        q4.tags.add(tag1)

        a1 = self.create_answer('Потому что гладиолус 1', user2, q1)
        a2 = self.create_answer('Потому что гладиолус 2', user3, q1)
        a3 = self.create_answer('Потому что гладиолус 3', user3, q1)
        a4 = self.create_answer('Потому что гладиолус 4', user2, q1)
        a5 = self.create_answer('Потому что гладиолус 5', user4, q1)
        a6 = self.create_answer('Потому что гладиолус 6', user4, q1)

        a7 = self.create_answer('Да кто его знает :0', user1, q2)
        a8 = self.create_answer('Не могу ответить емае', user3, q2)
        a9 = self.create_answer('Это очевидно друг мой', user3, q2)
        a10 = self.create_answer('hihi haha', user1, q2)
        a11 = self.create_answer('Потому что гладиолус 5', user4, q2)
        a12 = self.create_answer('Потому что гладиолус 6', user4, q2)

        self.like_question(q1, user2)
        self.like_question(q1, user3)
        self.dislike_question(q1, user4)

        self.like_answer(a1, user1)
        self.like_answer(a1, user2)
        self.like_answer(a3, user3)
        self.dislike_answer(a1, user3)

    def create_question(self, title, text, author):
        question = Question(title=title, text=text, author=author)
        question.save()

        return question

    def create_answer(self, text, author, question):
        answer = Answer(text=text, author=author, question=question)
        answer.save()

        return answer

    def like_question(self, question, user):
        like = LikeQuestion(like_or_dislike=LikeQuestion.LIKE, question=question, user=user)
        like.save()

    def dislike_question(self, question, user):
        like = LikeQuestion(like_or_dislike=LikeQuestion.DISLIKE, question=question, user=user)
        like.save()

    def like_answer(self, answer, user):
        like = LikeAnswer(like_or_dislike=LikeAnswer.LIKE, answer=answer, user=user)
        like.save()

    def dislike_answer(self, answer, user):
        like = LikeAnswer(like_or_dislike=LikeAnswer.DISLIKE, answer=answer, user=user)
        like.save()
