from django.urls import path
from . import views

urlpatterns = [
    path('lists/', views.todo_list, name='lists'), # For viewing all lists, adding a new list, deleting all lists
    path('lists/<int:pk>/', views.todo_detail, name="list"), # For viewing a specific list or deleting it
    path('lists/<int:pk>/items/', views.todo_add, name="list-items"), # For adding a new item to a list and viewing all items in a list
    path('lists/<int:pk>/items/<int:li>', views.todo_update, name="update-item"), # For updating an item in a list or deleting it
]