# Generated by Django 4.0.6 on 2022-07-29 09:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_alter_lessonstudent_homework_done_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='groupstudent',
            unique_together={('student', 'group')},
        ),
    ]
