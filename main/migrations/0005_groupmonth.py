# Generated by Django 4.0.6 on 2022-07-23 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_group_even'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_monthes', to='main.group')),
            ],
        ),
    ]
