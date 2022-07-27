# Generated by Django 4.0.6 on 2022-07-26 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_paid_by_parents'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='payer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]