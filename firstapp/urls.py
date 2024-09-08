from django.urls import path # type: ignore
from . import views
from django.http import HttpResponse # type: ignore

urlpatterns=[
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.rooms, name="room"),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom,name="delete-room"),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name='register'),
    path('delete-msg/<str:pk>/',views.deleteMsg,name="delete-msg"),
    path('profile/<str:pk>/',views.profile, name='user-profile'),
    path('edit-user/',views.editUser,name='edit-user'),
    path('topics/',views.topicsPage,name='topics'),
    path('activity/',views.activityPage,name='activity')
]