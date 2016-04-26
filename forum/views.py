from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from forum.forms import TopicForm, UserForm
from forum.models import Question, Answer


class TopicsIndexView(ListView):
    template_name = 'forum/topics/index.html'
    context_object_name = 'followed_topics_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated():
            topics = user.get_followed_topics()
        else:
            topics = []
        return topics

    def get_context_data(self, **kwargs):
        context = super(TopicsIndexView, self).get_context_data(**kwargs)

        form = TopicForm()
        context['form'] = form
        return context


class UsersFollowView(ListView):
    template_name = 'forum/users/index.html'
    context_object_name = 'followed_users_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated():
            users = user.get_followed_users()
        else:
            users = []
        return users

    def get_context_data(self, **kwargs):
        context = super(UsersFollowView, self).get_context_data(**kwargs)

        form = UserForm()
        context['form'] = form
        return context


class FeedIndexView(ListView):
    template_name = 'forum/feeds/index.html'
    context_object_name = 'feeds_list'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated():
            users = user.get_followed_users()
            topics = user.get_followed_topics()
        questions=Question.objects.filter(
            Q(topics__in=topics) | Q(asker__in=users)
        ).order_by('-created_at')

        return questions


class FeedQuestionAnswerView(ListView):

    template_name = 'forum/feeds/answers.html'
    context_object_name = 'answers_list'

    def get_queryset(self):
        user = self.request.user
        question_id = self.kwargs['question_id']
        question = get_object_or_404(
            Question, pk=question_id
        )
        self.question = question

        answers = Answer.objects.filter(question=question)
        return answers

    def get_context_data(self, **kwargs):
        context = super(FeedQuestionAnswerView, self).get_context_data(**kwargs)
        context['question'] = self.question
        return context
