from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AppUser
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
   # permission_classes = [permissions.AllowAny]
    queryset = AppUser.objects.all()
    serializer_class = RegisterSerializer

class MeView(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

from rest_framework_simplejwt.views import TokenObtainPairView


