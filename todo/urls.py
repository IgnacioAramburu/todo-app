from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view),
    path('logout',views.logout_view)
]