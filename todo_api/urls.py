from django.urls import path
from .views import UsersView, ToDoListView, ToDoItemView

urlpatterns = [
    path(r'users', UsersView.as_view(), name="user-view"),
    path(r'users/<str:user_email>', UsersView.as_view(), name="userview-with-mail"),
    path(r'lists', ToDoListView.as_view(), name="todolist-view"),
    path(r'lists/<int:id>', ToDoListView.as_view(), name="todolist-view"),
    path(r'lists/user/<str:user_email>', ToDoListView.as_view(), name="todolist-view"),
    path(r'lists/<int:id>/user/<str:user_email>', ToDoListView.as_view(), name="todolist-view"),
    path(r'items', ToDoItemView.as_view(), name="todoitem-view"),
    path(r'items/user/<str:user_email>', ToDoItemView.as_view(), name="todolist-view"),
    path(r'items/<int:id>', ToDoItemView.as_view(), name="todoitem-view"),
    path(r'items/list/<int:list_id>', ToDoItemView.as_view(), name="todoitem-view"),
    path(r'items/list/<int:list_id>/user/<str:user_email>', ToDoItemView.as_view(), name="todoitem-view"),
    path(r'items/<int:id>/user/<str:user_email>', ToDoItemView.as_view(), name="todolist-view"),
]