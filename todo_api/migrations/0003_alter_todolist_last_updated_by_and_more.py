# Generated by Django 5.0.2 on 2024-02-13 14:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_api', '0002_remove_todouser_profile_picture_url_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='last_updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RenameField(
            model_name='todoitem',
            old_name='list',
            new_name='list_id',
        ),
        migrations.DeleteModel(
            name='ToDoUser',
        ),
    ]
