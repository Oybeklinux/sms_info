# Generated by Django 4.0.6 on 2022-08-18 12:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_remove_user_payers_remove_user_payer_user_payer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='payer',
        ),
        migrations.AddField(
            model_name='user',
            name='parent',
            field=models.ManyToManyField(null=True, related_name='parents', to=settings.AUTH_USER_MODEL),
        ),
    ]
