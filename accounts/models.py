from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile


class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    credits = models.IntegerField(default=500, editable=False)

    def change_credits(self, creds):
        self.credits += creds
        if self.credits < 0:
            self.user.is_active = False
            self.user.save()
        self.save()
