from django.conf.urls import url

from forum.views import UsersFollowView

urlpatterns = [
    url(r'^$', UsersFollowView.as_view(), name='users_list'),
]
