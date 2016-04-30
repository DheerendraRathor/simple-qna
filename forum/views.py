import json

from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.edit import FormView

from forum.forms import TopicForm, UserForm, NewQuestionForm, NewAnswerForm
from forum.models import Question, Answer, Topic


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
            questions = Question.objects.filter(
                Q(topics__in=topics) | Q(asker__in=users) | Q(asker=user)
            ).order_by('-created_at')

        else:
            questions = []

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

        answers = Answer.objects.filter(question=question).annotate(upvotes_count=Count('upvotes'),
                                                                    downvotes_count=Count('downvotes'),
                                                                    )
        return answers

    def get_context_data(self, **kwargs):
        context = super(FeedQuestionAnswerView, self).get_context_data(**kwargs)
        context['question'] = self.question
        return context


class NewQuestionView(FormView):
    form_class = NewQuestionForm
    template_name = 'forum/feeds/new_question.html'
    success_url = '/feed/'

    def form_valid(self, form):
        question = form.save(commit=False)
        topics = form.cleaned_data['topics']
        question.asker = self.request.user
        question.save()
        topics = Topic.objects.filter(pk__in=topics)
        question.topics.add(*topics)
        return super(NewQuestionView, self).form_valid(form)


class NewAnswerView(FormView):
    form_class = NewAnswerForm
    template_name = 'forum/feeds/new_question.html'

    def get_success_url(self):
        question_id = self.kwargs.get('question_id')
        return '/feed/question/%s/' % question_id

    def form_valid(self, form):
        user = self.request.user
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        question.asker.profile.change_credits(10)
        answer = form.save(commit=False)
        answer.question = question
        answer.responder = user
        answer.save()
        return super(NewAnswerView, self).form_valid(form)


class AnswerVoteView(View):

    def post(self, request, answer_id, vote_type):

        answer = get_object_or_404(Answer, pk=answer_id)
        user = request.user

        if vote_type == 'upvote':
            answer.upvote(user)
        else:
            answer.downvote(user)

        qs = Answer.objects.filter(id=answer.id).aggregate(upvotes_count=Count('upvotes'),
                                                           downvotes_count=Count('downvotes'),
                                                           )
        return HttpResponse(
            json.dumps({
                'upvotes': qs['upvotes_count'],
                'downvotes': qs['downvotes_count'],
            }),
            content_type='application/json',
        )
