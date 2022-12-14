# Generated by Django 4.1.2 on 2022-11-12 00:55

import authors.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('follow', '0002_alter_follow_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='actor',
            field=models.URLField(validators=[authors.util.AuthorUtil.validate_author_url]),
        ),
        migrations.AlterField(
            model_name='follow',
            name='target',
            field=models.URLField(validators=[authors.util.AuthorUtil.validate_author_url]),
        ),
    ]
