# Generated by Django 4.0.6 on 2022-07-25 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_study_user_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='paid_by_parents',
            field=models.BooleanField(default=True),
        ),
    ]
