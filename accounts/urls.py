from django.urls import path

from .views import UserSearchViewSet

urlpatterns = [
    path('search/', UserSearchViewSet.as_view(), name='search')
]