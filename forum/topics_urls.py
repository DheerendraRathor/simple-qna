from django.conf.urls import url

from forum.views import TopicsIndexView

urlpatterns = [
    url(r'^$', TopicsIndexView.as_view(), name='topics_list'),
]
