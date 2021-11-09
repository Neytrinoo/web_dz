from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.db.models import Count, Q
from django.urls import reverse

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
        user_obj.save(using=self._db)
        return user_obj

    def get_best_users(self):
        users = super().get_queryset().annotate(count_questions=Count('question')).order_by('-count_questions')
        return users


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/')
    objects = UserManager()

    def get_absolute_url(self):
        return reverse('user', kwargs={'id': self.pk})


class TagManager(models.Manager):
    def get_popular_tags(self):
        tags = super().get_queryset().annotate(questions_count=Count('question')).order_by('-questions_count')
        return tags


class Tag(models.Model):
    title = models.CharField(max_length=32, primary_key=True)
    objects = TagManager()

    def get_absolute_url(self):
        return reverse('tag', kwargs={'title': self.title})


class QuestionManager(models.Manager):
    def get_best_questions(self):
        questions = super().get_queryset().annotate(count_likes=Count('like', filter=Q(like__like_or_dislike=LikeQuestion.LIKE))).order_by(
            '-count_likes')
        return questions

    def get_new_questions(self):
        return super().get_queryset().all().order_by('-date_publish')


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.CharField(max_length=DEFAULT_TEXT_LENGTH)
    date_publish = models.TimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='questions', related_query_name='question')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions', related_query_name='question')

    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse('question', kwargs={'id': self.pk})

    def get_count_likes(self):
        return self.likes.filter(like_or_dislike=LikeQuestion.LIKE).count()

    def get_count_dislikes(self):
        return self.likes.filter(like_or_dislike=LikeQuestion.DISLIKE).count()


class Answer(models.Model):
    text = models.CharField(max_length=DEFAULT_TEXT_LENGTH)
    date_publish = models.TimeField(auto_now_add=True)
    question = models.ForeignKey(Question, related_name='answers', related_query_name='answer', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers', related_query_name='answer')

    def get_count_likes(self):
        return self.likes.filter(like_or_dislike=LikeAnswer.LIKE).count()

    def get_count_dislikes(self):
        return self.likes.filter(like_or_dislike=LikeAnswer.DISLIKE).count()


class LikeAnswer(models.Model):
    LIKE = 1
    DISLIKE = 2
    LIKE_CHOICE = [(LIKE, 'LIKE'), (DISLIKE, 'DISLIKE')]
    like_or_dislike = models.PositiveSmallIntegerField(choices=LIKE_CHOICE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes', related_query_name='like', default=None)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes_answers', related_query_name='like_answer')


class LikeQuestion(models.Model):
    LIKE = 1
    DISLIKE = 2
    LIKE_CHOICE = [(LIKE, 'LIKE'), (DISLIKE, 'DISLIKE')]
    like_or_dislike = models.PositiveSmallIntegerField(choices=LIKE_CHOICE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes', related_query_name='like', default=None)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes_questions', related_query_name='like_question')
