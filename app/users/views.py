from .models import UserAccount
from .serializers import UserSerializer, TokenSerializer, PasswordSerializer, UpdateUserSerializer
from rest_framework import generics, permissions, status
from .permissions import IsAdminOrOwner
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserList(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {'GET': (permissions.IsAdminUser, )}

    def get_permissions(self):
        if self.request.method in self.permission_classes_by_action:
            return tuple([permission() for permission in self.permission_classes_by_action[self.request.method]])
        else:
            return tuple()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrOwner, )

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


class UpdateUser(generics.UpdateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAdminOrOwner,)

    def put(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 'me':
            self.kwargs['pk'] = request.user.pk
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 'me':
            self.kwargs['pk'] = request.user.pk
        return self.partial_update(request, *args, **kwargs)


class ChangePassword(UpdateUser):
    serializer_class = PasswordSerializer

    def patch(self, request, *args, **kwargs):
        return Response({'detail': f'Method \"PATCH\" not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
