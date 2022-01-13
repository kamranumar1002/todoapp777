from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('deletetask/<int:id>', views.deleteTask, name='deleteTask'),
    path('edittask/<int:id>', views.edittask, name='edittask'),
    path('addtask', views.addtask, name='addtask'),
    path('login', views.loginUser, name='login'),
    path('register', views.registerUser, name='register'),
    path('logout', views.logoutUser, name='logout'),
]