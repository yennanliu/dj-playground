# Generated by Django 2.1.5 on 2019-01-20 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_merge_20190120_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletedmessage',
            name='content',
            field=models.CharField(blank=True, help_text='The content of this message, taken from Discord.', max_length=2000),
        ),
    ]
