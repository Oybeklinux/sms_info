# Generated by Django 4.0.6 on 2022-07-19 12:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_lessonstudent_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonstudent',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
