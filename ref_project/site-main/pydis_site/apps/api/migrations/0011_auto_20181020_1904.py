# Generated by Django 2.1.2 on 2018-10-20 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_snakeidiom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snakeidiom',
            name='idiom',
            field=models.CharField(help_text='A saying about a snake.', max_length=140, primary_key=True, serialize=False),
        ),
    ]
