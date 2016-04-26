from django.conf.urls import url

from forum.views import FeedIndexView

urlpatterns = [
    url(r'^$', FeedIndexView.as_view(), name='user_feeds'),
]
