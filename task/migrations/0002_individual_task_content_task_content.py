# Generated by Django 4.2.7 on 2023-11-07 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual_task',
            name='content',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='task',
            name='content',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
