# Generated by Django 4.0.6 on 2022-07-29 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_groupstudent_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='groupstudent',
            unique_together=set(),
        ),
    ]
