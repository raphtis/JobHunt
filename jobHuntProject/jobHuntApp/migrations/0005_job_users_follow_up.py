# Generated by Django 2.2 on 2021-11-01 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobHuntApp', '0004_auto_20211030_0419'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='users_follow_up',
            field=models.ManyToManyField(related_name='jobs_users_marked', to='jobHuntApp.User'),
        ),
    ]