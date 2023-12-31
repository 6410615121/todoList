# Generated by Django 4.2.7 on 2023-11-06 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='todoUser',
            fields=[
                ('todoUser_ID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Firstname', models.CharField(max_length=50)),
                ('Lastname', models.CharField(max_length=50)),
                ('friends', models.ManyToManyField(blank=True, to='user.todouser')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friend_request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='user.todouser')),
                ('To_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='user.todouser')),
            ],
        ),
    ]
