# Generated by Django 4.1.2 on 2022-11-12 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follow', '0003_alter_follow_actor_alter_follow_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='remote_url',
            field=models.URLField(blank=True),
        ),
    ]
