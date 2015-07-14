from rest_framework import viewsets
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework import status
from accounts.models import PushUser
from accounts.serializers import CreateUserSerializer, UserSerializer
from rest_framework import permissions
from rest_framework.authtoken.models import Token


class AccountViewSet(viewsets.ViewSet):

    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer

    def retrieve(self, request, pk=None):
        try:
            user = PushUser.objects.get(pk=pk)
        except PushUser.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        if user.pk != request.user.pk:
            return Response(status.HTTP_403_FORBIDDEN)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    def list(self, request):
        return self.retrieve(request, request.user.pk)

    def create(self, request):
        serializer = CreateUserSerializer(data=request.DATA)
        if serializer.is_valid():
            email = serializer.data.get('email', None)
            username = serializer.data['username']
            password = serializer.data['password']
            try:
                existing_user = PushUser.objects.get(username=username)
            except PushUser.DoesNotExist:
                existing_user = None
            if existing_user is not None:
                return obtain_auth_token(request)
            if email is not None and len(email) > 0:
                existing_users = PushUser.objects.filter(email=email)
                if len(existing_users) > 0:
                    return Response({'error': 'An account with that email address already exists.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            user = PushUser.objects.create_user(email=email, username=username, password=password)
            user.save()
            token = Token.objects.create(user=user)
            user_serializer = UserSerializer(user)
            response_data = user_serializer.data
            response_data['token'] = token.key
            return Response(response_data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
