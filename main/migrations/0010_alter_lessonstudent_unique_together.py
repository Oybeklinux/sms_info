# Generated by Django 4.0.6 on 2022-07-23 09:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0009_alter_groupmonth_month'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lessonstudent',
            unique_together={('student', 'lesson')},
        ),
    ]