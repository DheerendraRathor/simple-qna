from django.views.generic import ListView

from forum.forms import TopicForm, UserForm


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
        return []
