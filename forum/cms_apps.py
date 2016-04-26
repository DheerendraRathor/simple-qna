from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class TopicsApphook(CMSApp):
    name = _("Topics Application")   # give your application a name (required)
    urls = ["forum.topics_urls"]           # link your app to url configuration(s)
    app_name = "forum"


class FeedApphook(CMSApp):
    name = _("Feed")
    urls = ["forum.feed_urls"]
    app_name = "forum2"


class UsersApphook(CMSApp):
    name = _("User")
    urls = ["forum.users_urls"]
    app_name = "forum3"


apphook_pool.register(TopicsApphook)  # register the application
apphook_pool.register(FeedApphook)
apphook_pool.register(UsersApphook)
