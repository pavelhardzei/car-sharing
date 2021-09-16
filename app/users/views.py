from .models import UserAccount
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsAdminOrOwner
from rest_framework.authentication import TokenAuthentication


class UserRegister(generics.CreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (TokenAuthentication, )


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrOwner]
    authentication_classes = (TokenAuthentication, )
