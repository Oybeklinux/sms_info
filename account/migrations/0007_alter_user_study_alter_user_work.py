# Generated by Django 4.0.6 on 2022-07-27 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_payer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='study',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='work',
            field=models.BooleanField(default=None, null=True),
        ),
    ]