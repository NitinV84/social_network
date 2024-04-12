from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

"""
these are the urls for friends app
"""
urlpatterns = [
    path('friend_list/', ListFriends.as_view()),
    path('friendrequest/', FriendRequestViewSet.as_view()),
    path('status/<int:pk>/', UpdateFriendRequestStatus.as_view()),
]