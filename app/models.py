from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.db.models import Count, Q
from django.urls import reverse
from datetime import datetime

DEFAULT_TEXT_LENGTH = 10000


class UserManager(BaseUserManager):
    def create_user(self, email, password, username, avatar=None):
        pre_user = User(email=email, username=username)
        pre_user.set_password(password)
        pre_user.save()
        user_obj = self.model(
            user=pre_user
        )
        if avatar is not None:
            user_obj.avatar = avatar
        return user_obj

    def get_best_users(self):
        users = super().get_queryset().annotate(count_questions=Count('question')).order_by('-count_questions')
        return users


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/')
    objects = UserManager()

    def get_absolute_url(self):
        return reverse('user', kwargs={'id': self.pk})


class TagManager(models.Manager):
    def get_popular_tags(self):
        tags = super().get_queryset().annotate(questions_count=Count('question')).order_by('-questions_count')
        return tags


class Tag(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=32, unique=True)
    objects = TagManager()

    def get_absolute_url(self):
        return reverse('tag', kwargs={'title': self.title})


class QuestionManager(models.Manager):
    def get_best_questions(self):
        questions = super().get_queryset().order_by('-count_likes')
        return questions

    def get_new_questions(self):
        return super().get_queryset().order_by('-date_publish')


class Question(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=256)
    text = models.CharField(max_length=DEFAULT_TEXT_LENGTH)
    date_publish = models.DateField(default=datetime.now())
    tags = models.ManyToManyField(Tag, related_name='questions', related_query_name='question')
    author = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='questions', related_query_name='question')
    count_likes = models.IntegerField(default=0)
    count_dislikes = models.IntegerField(default=0)

    objects = QuestionManager()

    def like(self):
        self.count_likes += 1

    def dislike(self):
        self.count_dislikes += 1

    def get_absolute_url(self):
        return reverse('question', kwargs={'id': self.pk})

    def get_count_likes(self):
        return self.count_likes

    def get_count_dislikes(self):
        return self.count_dislikes

    def get_date_publish(self):
        return self.date_publish


class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=DEFAULT_TEXT_LENGTH)
    date_publish = models.DateField(default=datetime.now())
    question = models.ForeignKey(Question, related_name='answers', related_query_name='answer', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers', related_query_name='answer')
    count_likes = models.IntegerField(default=0)
    count_dislikes = models.IntegerField(default=0)

    def like(self):
        self.count_likes += 1

    def dislike(self):
        self.count_dislikes += 1

    def get_count_likes(self):
        return self.count_likes

    def get_count_dislikes(self):
        return self.count_dislikes

    def get_date_publish(self):
        return str(self.date_publish)


class LikeAnswer(models.Model):
    id = models.IntegerField(primary_key=True)
    LIKE = 1
    DISLIKE = 2
    LIKE_CHOICE = [(LIKE, 'LIKE'), (DISLIKE, 'DISLIKE')]
    like_or_dislike = models.PositiveSmallIntegerField(choices=LIKE_CHOICE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes', related_query_name='like', default=None)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes_answers', related_query_name='like_answer')


class LikeQuestion(models.Model):
    id = models.IntegerField(primary_key=True)
    LIKE = 1
    DISLIKE = 2
    LIKE_CHOICE = [(LIKE, 'LIKE'), (DISLIKE, 'DISLIKE')]
    like_or_dislike = models.PositiveSmallIntegerField(choices=LIKE_CHOICE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes', related_query_name='like', default=None)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes_questions', related_query_name='like_question')
