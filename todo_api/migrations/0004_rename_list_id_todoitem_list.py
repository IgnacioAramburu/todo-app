# Generated by Django 5.0.2 on 2024-02-13 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_api', '0003_alter_todolist_last_updated_by_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todoitem',
            old_name='list_id',
            new_name='list',
        ),
    ]
