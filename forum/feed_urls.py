from django.conf.urls import url

from forum.views import FeedIndexView, FeedQuestionAnswerView, NewQuestionView, NewAnswerView, AnswerVoteView

urlpatterns = [
    url(r'^$', FeedIndexView.as_view(), name='user_feeds'),
    url(r'^new/$', NewQuestionView.as_view(), name='new_question'),
    url(r'^question/(?P<question_id>\d+)/$', FeedQuestionAnswerView.as_view(), name='question_answers'),
    url(r'^question/(?P<question_id>\d+)/new/$', NewAnswerView.as_view(), name='add_answer'),
    url(r'^answer/(?P<answer_id>\d+)/(?P<vote_type>(upvote)|(downvote))/$',
        AnswerVoteView.as_view(), name='add_votes')
]
