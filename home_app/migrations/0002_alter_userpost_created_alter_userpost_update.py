# Generated by Django 5.0.6 on 2024-06-01 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
