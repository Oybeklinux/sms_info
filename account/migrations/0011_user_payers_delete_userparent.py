# Generated by Django 4.0.6 on 2022-08-18 12:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_user_payer_userparent'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='payers',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserParent',
        ),
    ]