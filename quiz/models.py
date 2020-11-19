from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.template.defaultfilters import slugify


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    roll_out = models.BooleanField(default=False)
    slug = models.SlugField()

    class Meta:
        ordering = ["created"]

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    label = models.CharField(max_length=500)
    order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.label


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.text


class QuizTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Response(models.Model):
    quiztaker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question.label


@receiver(pre_save, sender=Quiz)
def slugify_title(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


""" @receiver(post_save, sender=Quiz)
def set_default(sender, instance, created, **kwargs):
    quiz = Quiz.objects.filter(id=instance.quiz.id)
 """
