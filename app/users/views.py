from .models import UserAccount
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsAdminOrOwner


class UserRegister(generics.CreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrOwner]
