# Generated by Django 3.2.7 on 2021-09-12 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0002_contactmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='post_view',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
