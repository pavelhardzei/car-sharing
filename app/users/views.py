from .models import UserAccount
from .serializers import UserSerializer, TokenSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsAdminOrOwner
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserRegister(generics.CreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )
    authentication_classes = (TokenAuthentication, )


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrOwner, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 'me':
            self.kwargs['pk'] = request.user.pk
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 'me':
            self.kwargs['pk'] = request.user.pk
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 'me':
            self.kwargs['pk'] = request.user.pk
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 'me':
            self.kwargs['pk'] = request.user.pk
        return self.destroy(request, *args, **kwargs)


class AuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name': user.name
        })
