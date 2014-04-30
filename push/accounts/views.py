from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from accounts.models import PushUser
from accounts.serializers import CreateUserSerializer, UserSerializer
from apps.models import PushApplication
from rest_framework import permissions


class AccountViewSet(viewsets.ViewSet):

    permission_classes = (permissions.AllowAny,)

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
            client_id = serializer.data['client_id']
            try:
                application = PushApplication.objects.get(client_id=client_id)
            except PushApplication.DoesNotExist:
                return Response({'error': 'Application does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)
            email = serializer.data['email']
            username = serializer.data['username']
            password = serializer.data['password']
            error = {'error': 'Account already exists.'}
            try:
                existing_user = PushUser.objects.get(username=username)
            except PushUser.DoesNotExist:
                existing_user = None
            if existing_user is not None:
                return Response(error,
                                status=status.HTTP_400_BAD_REQUEST)
            if len(email) > 0:
                existing_users = PushUser.objects.filter(app__pk=application.pk, email=email)
                if len(existing_users) > 0:
                    return Response(error,
                                    status=status.HTTP_400_BAD_REQUEST)
            user = PushUser.objects.create_user(email=email, username=username, password=password)
            user.app = application
            user.save()
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
