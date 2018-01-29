# Generated by Django 2.0 on 2018-01-28 09:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query_utils
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('game', '0014_auto_20180128_0957'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('read', models.BooleanField(default=True)),
                ('msg', models.CharField(max_length=200)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('character_type', models.ForeignKey(limit_choices_to=django.db.models.query_utils.Q(django.db.models.query_utils.Q(('app_label', 'character'), ('model', 'Player'), _connector='AND'), django.db.models.query_utils.Q(('app_label', 'character'), ('model', 'NPC'), _connector='AND'), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='game.Game')),
            ],
        ),
    ]
