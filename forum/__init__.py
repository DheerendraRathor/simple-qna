from django.apps import AppConfig, apps
from django.contrib.auth import get_user_model


class ForumConfig(AppConfig):
    name = 'forum'

    def ready(self):
        import followit
        Topic = apps.get_model('forum.Topic')
        followit.register(Topic)
        followit.register(get_user_model())

default_app_config = 'forum.ForumConfig'
