from django.urls import path
from base.views import (
    home,
    room,
    createRoom,
    updateRoom,
    deleteRoom,
    loginPage,
    registerPage,
    logoutUser,
    deleteMessage,
    userProfile
)

urlpatterns = [
    path(route='login/', view=loginPage, name='login'), 
    path(route='register/', view=registerPage, name='register'), 
    path(route='logout/', view=logoutUser, name='logout'), 
    
    path(route='profile/<str:pk>/', view=userProfile, name='user-profile'),
    
    path(route='', view=home, name='home'),
    path(route='room/<str:pk>/', view=room, name='room'),
    path(route='create-room/', view=createRoom, name='create-room'),
    path(route='update-room/<str:pk>/', view=updateRoom, name='update-room'),
    path(route='delete-room/<str:pk>/', view=deleteRoom, name='delete-room'),
    path(route='delete-message/<str:pk>/', view=deleteMessage, name='delete-message')
]
