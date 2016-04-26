from ajax_select import register, LookupChannel
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q

from .models import Topic


@register('topics')
class TopicsLookup(LookupChannel):
    model = Topic
    min_length = 3

    def check_auth(self, request):
        if not request.user.is_authenticated():
            raise PermissionDenied

    def get_query(self, q, request):
        self.request = request
        return self.model.objects.filter(name__icontains=q).order_by('name')[:50]

    def format_item_display(self, obj):

        toggle_follow_url = reverse('toggle_follow_object', args=['topic', obj.id])
        button = ''
        user = self.request.user
        if user.is_authenticated():
            if user.is_following(obj):
                follow = 'Unfollow'
            else:
                follow = 'Follow'
            button = u"""
            <button class="btn btn-primary toggle-follow" data-url="%s">
                %s
            </button>
            """ % (toggle_follow_url, follow)

        html = u'''
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <h4 class='col-md-6' style="padding-left: 0px;">%s</h4>
                        <div class="col-md-2">
                            %s
                        </div>
                    </div>
                    <div class="col-md-12">
                        <span>%s</span>
                    </div>
                </div>
            </div>
            ''' % (obj.name, button, obj.description)
        return html

    def format_match(self, obj):
        html = u'''
        <div>
            <h4>%s</h4>
            <p>%s</p>
        </div>
        ''' % (obj.name, obj.description)
        return html


@register('users')
class UsersLookup(LookupChannel):
    model = get_user_model()
    min_length = 3

    def check_auth(self, request):
        if not request.user.is_authenticated():
            raise PermissionDenied

    def get_query(self, q, request):
        self.request = request
        return self.model.objects.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(email__icontains=q)
        ).order_by('username')[:50]

    def format_item_display(self, obj):

        toggle_follow_url = reverse('toggle_follow_object', args=['user', obj.id])
        button = ''
        user = self.request.user
        if user.is_authenticated():
            if user.is_following(obj):
                follow = 'Unfollow'
            else:
                follow = 'Follow'
            button = u"""
            <button class="btn btn-primary toggle-follow" data-url="%s">
                %s
            </button>
            """ % (toggle_follow_url, follow)

        html = u'''
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <h4 class='col-md-6' style="padding-left: 0px;">%s</h4>
                        <div class="col-md-2">
                            %s
                        </div>
                    </div>
                    <div class="col-md-12">
                        <span>%s &lt;%s&gt;</span>
                    </div>
                </div>
            </div>
            ''' % (obj.username, button, obj.get_full_name(), obj.email)
        return html

    def format_match(self, obj):
        html = u'''
        <div>
            <p>%s &lt;%s&gt;</p>
            <span>%s</span>
        </div>
        ''' % (obj.username, obj.get_full_name(), obj.email)
        return html
