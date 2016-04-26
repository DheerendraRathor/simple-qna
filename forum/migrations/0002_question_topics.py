# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='topics',
            field=models.ManyToManyField(related_name='questions', to='forum.Topic', blank=True),
        ),
    ]
