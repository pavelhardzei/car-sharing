from .models import UserAccount
from .serializers import UserSerializer
from rest_framework import generics


class UserList(generics.ListAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
