from django.urls import path
from .views import UsersView, ToDoListView, ToDoItemView

urlpatterns = [
    path(r'users/', UsersView.as_view(), name="users"),
    path(r'list/', ToDoListView.as_view(), name="users"),
    path(r'item/', ToDoItemView.as_view(), name="users")
]