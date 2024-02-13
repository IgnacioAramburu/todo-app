from django.db import models
from django.contrib.auth.models import User
from datetime import date

class ToDoUser(User):
    list_count = models.IntegerField(default=0)

class ToDoList(models.Model):
    title = models.CharField(null=False, blank=False, max_length=50)
    description = models.CharField(max_length=200)
    completed = models.BooleanField(default=True)
    size = models.IntegerField(default=0)
    created_at = models.DateField(default=date.today)
    last_updated_at = models.DateField(default=date.today)
    last_updated_by = models.ForeignKey(ToDoUser, on_delete=models.CASCADE)

class ToDoItem(models.Model):
    title = models.CharField(null=False, blank=False, max_length=50)
    description = models.CharField(max_length=400)
    completed = models.BooleanField(default=False)
    created_at = models.DateField(default=date.today)
    last_updated_at = models.DateField(default=date.today)
    list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
