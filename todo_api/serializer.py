from rest_framework import serializers
from .models import ToDoUser, ToDoList, ToDoItem

class ToDoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoUser
        fields = '__all__'
