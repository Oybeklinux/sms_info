# Generated by Django 4.0.6 on 2022-07-19 09:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('start_time', models.TimeField()),
                ('duration_hours', models.FloatField(default=1.5)),
                ('duration_monthes', models.IntegerField(default=6)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('theme', models.CharField(max_length=300)),
                ('comment', models.CharField(max_length=300)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.group')),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LessonStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework_done', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.student')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='specialty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.specialty'),
        ),
        migrations.AddField(
            model_name='group',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.teacher'),
        ),
    ]
