from django.conf.urls import url

from forum.views import FeedIndexView, FeedQuestionAnswerView

urlpatterns = [
    url(r'^$', FeedIndexView.as_view(), name='user_feeds'),
    url(r'^question/(?P<question_id>\d+)/$', FeedQuestionAnswerView.as_view(), name='question_answers'),
]
