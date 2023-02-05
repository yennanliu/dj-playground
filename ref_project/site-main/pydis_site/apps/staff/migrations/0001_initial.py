# Generated by Django 2.2.6 on 2019-10-03 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('api', '0043_infraction_hidden_warnings_to_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoleMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(help_text='The Django permissions group to use for this mapping.', on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('role', models.OneToOneField(help_text='The Discord role to use for this mapping.', on_delete=django.db.models.deletion.CASCADE, to='api.Role')),
            ],
        ),
    ]
