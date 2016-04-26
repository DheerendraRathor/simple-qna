
from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Topic(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=512)
    description = models.TextField()
    topics = models.ManyToManyField(Topic, blank=True, related_name='questions')
    asker = models.ForeignKey(User, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    answer = models.TextField(null=True)
    responder = models.ForeignKey(User, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, blank=True, related_name='upvoted_answers')
    downvotes = models.ManyToManyField(User, blank=True, related_name='downvoted_answers')

    def upvote(self, user):
        self.downvotes.remove(user)
        if self.upvotes.filter(id=user.id).exists():
            self.upvotes.remove(user)
        else:
            self.upvotes.add(user)

    def downvote(self, user):
        self.upvotes.remove(user)
        if self.downvotes.filter(id=user.id).exists():
            self.downvotes.remove(user)
        else:
            self.downvotes.add(user)
