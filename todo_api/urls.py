from django.urls import path
from .views import ToDoListView, ToDoItemView

urlpatterns = [
    path(r'lists', ToDoListView.as_view(), name="todolist-view"),
    path(r'lists/<int:id>', ToDoListView.as_view(), name="todolist-view"),
    path(r'items', ToDoItemView.as_view(), name="todoitem-view"),
    path(r'items/<int:id>', ToDoItemView.as_view(), name="todoitem-view"),
    path(r'items/list/<int:list_id>', ToDoItemView.as_view(), name="todoitem-view"),
]