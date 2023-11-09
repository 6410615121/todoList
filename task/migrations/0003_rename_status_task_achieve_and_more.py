# Generated by Django 4.2.7 on 2023-11-07 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_individual_task_content_task_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='status',
            new_name='achieve',
        ),
        migrations.RemoveField(
            model_name='individual_task',
            name='content',
        ),
        migrations.RemoveField(
            model_name='task',
            name='content',
        ),
        migrations.AddField(
            model_name='individual_task',
            name='category',
            field=models.CharField(choices=[('category1', 'due'), ('category2', 'pastdue'), ('category3', 'complete')], default='category1', max_length=20),
        ),
        migrations.AddField(
            model_name='individual_task',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('category1', 'due'), ('category2', 'pastdue'), ('category3', 'complete')], default='category1', max_length=20),
        ),
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
