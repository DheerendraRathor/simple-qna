from django.contrib import admin
from django.db.models import Count

from forum.models import Topic, Answer, Question


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'created_at']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'created_at', 'upvote_count', 'downvote_count']

    def get_queryset(self, request):
        base_qs = super(AnswerAdmin, self).get_queryset(request)
        qs = base_qs.annotate(upvote_count=Count('upvotes'), downvote_count=Count('downvotes'))
        return qs

    def upvote_count(self, obj):
        return obj.upvote_count

    def downvote_count(self, obj):
        return obj.downvote_count


admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
