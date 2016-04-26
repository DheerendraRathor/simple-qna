# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_question_topics'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer',
            field=models.TextField(null=True),
        ),
    ]
