from ajax_select.fields import AutoCompleteSelectMultipleField
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model

from forum.models import Topic


class TopicForm(forms.ModelForm):

    topics = AutoCompleteSelectMultipleField('topics')

    class Meta:
        model = Topic
        fields = ['topics']


class UserForm(forms.ModelForm):

    users = AutoCompleteSelectMultipleField('users')

    class Meta:
        model = get_user_model()
        fields = ['users']
