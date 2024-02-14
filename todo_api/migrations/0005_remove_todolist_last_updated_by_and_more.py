# Generated by Django 5.0.2 on 2024-02-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_api', '0004_rename_list_id_todoitem_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='last_updated_by',
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='description',
            field=models.CharField(default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
    ]