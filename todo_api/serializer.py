from rest_framework.exceptions import APIException
from rest_framework import serializers
from .models import ToDoList, ToDoItem
from datetime import date

class ToDoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        fields = '__all__'

    def create(self,validated_data):
        validated_data.pop('created_at',None)
        validated_data.pop('last_updated_at',None)
        
        return super().create(validated_data)

    def update(self,instance,validated_data):
        validated_data.pop('created_at',None)
        validated_data.pop('list',None)
        validated_data['last_updated_at'] = date.today()
        return super().update(instance,validated_data)

class ToDoListSerializer(serializers.ModelSerializer):
    todoitem_set = ToDoItemSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = ToDoList
        fields = '__all__'

    def to_representation(self, instance):
        include_items = self.context.get('include_items')

        if include_items:
            return super().to_representation(instance)
        else:
            data = super().to_representation(instance)
            data.pop('todoitem_set', None)
            return data

    def create(self,validated_data):
        validated_data.pop('completed', None)
        validated_data.pop('size',None)
        validated_data.pop('created_at',None)
        validated_data.pop('last_updated_at',None)
        
        return super().create(validated_data)

    def update(self,instance,validated_data):
        validated_data.pop('created_at',None)
        validated_data['last_updated_at'] = date.today()     
        return super().update(instance,validated_data)
