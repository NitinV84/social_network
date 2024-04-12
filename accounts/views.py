from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import RegisterSerializer, ObtainTokenPairSerializer, UserSerializer


class ObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = ObtainTokenPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    User Registration view, handles signup
    """
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserSearchViewSet(APIView):
    """
    View returns users searched by name or email.
    """
    model = CustomUser
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request):
        user_search = request.GET.get('search', '')
        if user_search:
            search_result = self.model.objects.filter(
                Q(email__iexact=user_search) | 
                Q(first_name__icontains=user_search) |
                Q(last_name__icontains=user_search)
            )
            if search_result.exists():
                serialized_data = UserSerializer(search_result, many=True)
                return Response(serialized_data.data, 
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "User not found"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            serialized_data = UserSerializer(self.get_queryset(), many=True)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
