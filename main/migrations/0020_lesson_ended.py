# Generated by Django 4.0.6 on 2022-08-05 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_groupstudent_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='ended',
            field=models.BooleanField(default=False),
        ),
    ]
