from django.db import models
from datetime import date

class ToDoList(models.Model):
    title = models.CharField(null=False, blank=False, max_length=50)
    description = models.CharField(null=False, default="", max_length=200)
    completed = models.BooleanField(default=True)
    size = models.IntegerField(default=0)
    created_at = models.DateField(default=date.today)
    last_updated_at = models.DateField(default=date.today)

class ToDoItem(models.Model):
    title = models.CharField(null=False, blank=False, max_length=50)
    description = models.CharField(null=False, default="", max_length=400)
    completed = models.BooleanField(default=False)
    created_at = models.DateField(default=date.today)
    last_updated_at = models.DateField(default=date.today)
    list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
